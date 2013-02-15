class openresty {

  $version = '2.4.15'
  $download = "http://agentzh.org/misc/nginx/ngx_openresty-${version}.tar.gz"
  $dest = "/opt/ngx_openresty-${version}"
  $bin = '/usr/local/bin'

  exec { 'download-openresty':
    cwd     => '/tmp',
    command => "/usr/bin/wget -q ${download} -O ngx_openresty-${version}.tar.gz",
    timeout => 300,
    unless => "/usr/bin/test -f /tmp/ngx_openresty-${version}.tar.gz"
  }

  exec { 'extract-openresty':
    cwd     => '/tmp',
    command => "/bin/tar xzf /tmp/ngx_openresty-${version}.tar.gz",
    creates => "/tmp/ngx_openresty-${version}",
    require => Exec[download-openresty]
  }

  exec { "make-openresty":
    command => "./configure --with-luajit && /usr/bin/make && /usr/bin/make install PREFIX=${dest}",
    cwd     => "/tmp/ngx_openresty-${version}",
    creates => "/usr/local/openresty",
    require => [
      Exec[extract-openresty],
      Package['libncurses'],
      Package['libpcre'],
      Package['libreadline'],
      Package['libssl'],
      Package['perl'],
    ],
  }

}
