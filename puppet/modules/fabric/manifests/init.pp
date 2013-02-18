class fabric {
  package { 'Fabric':
    provider => 'pip',
    ensure   => 'present',
    requires => Package['python-dev'],
  }
}
