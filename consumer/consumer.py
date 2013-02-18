import os
import requests
from hotworker import HotWorkerBase
from hotqueue import HotQueue
import sys

BASE_DIR = '/var/www'


class CheeseShopWorker(HotWorkerBase):

    def __init__(self):
        self.base_path = '/simple/'
        self.pypi_url = 'http://pypi.python.org/'
        super(CheeseShopWorker, self).__init__()

    @property
    def queue_name(self):
        return self.get_queue.key

    def get_queue(self):
        return HotQueue('cheeseshop', serializer=None)

    def local_file_path(self, package, version, ext='tar.gz'):
        return os.path.join(
            BASE_DIR, self.base_path.replace('/', ''),
            package, '{}-{}.{}'.format(package, version, ext)
        )

    def local_file_exists(self, package, version):
        path = self.local_file_path(package, version)
        # this will catch most local files
        if os.path.exists(path):
            return True
        else:
            cached_packages = [filename.lower()
                for filename in os.listdir(os.path.dirname(path))]
            # this will catch case-difference issues
            if os.path.basename(path).lower() in cached_packages:
                return True
            else:
                # this will catch stray zip files
                zip_path = self.local_file_path(package, version, 'zip')
                if os.path.basename(zip_path).lower() in cached_packages:
                    return True
        return False

    def get_package_name_and_version(self, path):
        parts = path.strip('/').split('/')
        if len(parts) == 1:
            return (parts[0], None)
        return (parts[0], parts[-1])

    def construct_pypi_api_url(self, package, version):
        pypi_api_url = '{}pypi/{}'.format(self.pypi_url, package)
        if version is not None:
            pypi_api_url = '{}/{}'.format(pypi_api_url, version)
        return '{}/{}'.format(pypi_api_url, 'json')

    def get_download_url(self, package, version):
        pypi_api_url = self.construct_pypi_api_url(package, version)
        r = requests.get(pypi_api_url)
        # if we can't get information, maybe the package doesn't exist
        # pip install will have provided an error to the user earlier
        if r.status_code != 200:
            # it might be that the case of some letters are wrong
            # so let's see if pypi simple does a redirect
            # which will give us the right name
            print '    > trying url {}simple/{}/'.format(
                self.pypi_url, package)
            r = requests.head('{}simple/{}/'.format(
                self.pypi_url, package), allow_redirects=False)
            if r.status_code == 301:
                real_package = r.headers.get('location').split('/')[-1]
                print '    > {} redirected to {}'.format(package, real_package)
                pypi_api_url = self.construct_pypi_api_url(
                    real_package, version)
                r = requests.get(pypi_api_url)

        # we might have a new status code if our name change was successful
        if r.status_code == 200:
            r_json = r.json()
            # try a couple of places that a download url might be found
            try:
                urls = r_json['urls']
                download_url = next(url['url'] for url in urls
                    if url['url'].endswith(('tar.gz', '.zip')))
            except IndexError:
                download_url = r_json['info']['download_url']

            if not download_url.startswith('http://'):
                return None
            else:
                return download_url

    def cache_package_locally(self, package, download_url):
        r = requests.get(download_url)
        if r.status_code == 200:
            path = os.path.join(
                BASE_DIR, self.base_path.replace('/', ''),
                package, os.path.basename(download_url)
            )
            dirs_path = os.path.dirname(path)
            if not os.path.exists(dirs_path):
                os.makedirs(dirs_path)
            with open(path, 'wb+') as f:
                f.write(r.content)
                print '    > {} written to path'.format(path)

    def process_item(self, message):
        # ignore anything ending with a /
        # as it's a duplicate
        if not message.endswith('/'):
            # trim the path down to just package (and possibly version)
            path = message.replace(self.base_path, '')
            package, version = self.get_package_name_and_version(path)
            print package, version
            # if there's no version requested there aren't any local files
            # if there is a version then check to see if we have it already
            if version is None or not self.local_file_exists(package, version):
                print '    > no cached version for {} ({})'.format(
                                                    package, version)
                download_url = self.get_download_url(package, version)
                # if we can find a download url, then try to cache the package
                if download_url is not None:
                    #print 'download url found'
                    self.cache_package_locally(package, download_url)
                else:
                    #print 'no download url found for {}=={}'.format(
                    #                                package, version)
                    pass
            else:
                #print 'cached version of {}=={} exists'.format(
                #                                    package, version)
                pass


def main():

    import argparse

    parser = argparse.ArgumentParser(
        description="Consume messages from cheeseshop queue "
                    "and get packages from pypi if necessary")
    parser.parse_args()

    csw = CheeseShopWorker()
    csw()


if __name__ == '__main__':
    main()
