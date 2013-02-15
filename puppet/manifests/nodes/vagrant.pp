#
# Standalone manifest - for dev Vagrant box.
#
node "vagrant-ubuntu-precise-64" {

  include common
  include vagrant
  include vagrant::puppet

}
