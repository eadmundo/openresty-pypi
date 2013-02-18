class hotworker {
  package { 'hotworker':
    provider => 'pip',
    ensure   => '0.2.0',
    requires => Package['python-dev'],
  }
}
