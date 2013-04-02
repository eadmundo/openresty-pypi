# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "precise64"

  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  # Update apt
  config.vm.provision :shell, :inline => "aptitude -q2 update"

  # make sure puppet is installed
  config.vm.provision :shell, :inline => "apt-get install -y puppet"

  # Puppet bootstrap - update apt cache
  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "puppet/manifests"
    puppet.module_path = "puppet/modules"
    puppet.manifest_file  = "bootstrap/apt-update.pp"
  end

  config.vm.define :deploy do |deploy_config|

    deploy_config.vm.provider :aws do |aws|

      aws.access_key_id = ENV['AWS_ACCESS_KEY_ID']
      aws.secret_access_key = ENV['AWS_SECRET_ACCESS_KEY']
      aws.keypair_name = "soma"
      aws.ssh_private_key_path = ENV['AWS_SOMA_PRIVATE_KEY_PATH']
      aws.region = 'eu-west-1'
      aws.ami = "ami-e7b6b393"
      aws.ssh_username = "ubuntu"
      aws.tags = { :Name => 'openresty-pypi' }

    end

  end

  config.vm.define :develop do |develop_config|

    develop_config.vm.network :private_network, ip: "173.16.1.2"
    develop_config.vm.network :forwarded_port, guest: 8080, host: 8080
    develop_config.vm.synced_folder ".", "/vagrant", :nfs => true

    # Puppet bootstrap - install augeas
    develop_config.vm.provision :puppet do |puppet|
      puppet.manifests_path = "puppet/manifests"
      puppet.module_path = "puppet/modules"
      puppet.manifest_file  = "bootstrap/vagrant-puppet.pp"
    end

  end

  # Puppet stand alone.
  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "puppet/manifests"
    puppet.module_path = "puppet/modules"
    puppet.manifest_file  = "site.pp"
  end

end
