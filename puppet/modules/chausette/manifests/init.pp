class chaussette {

  package { 'chaussette':
    provider => 'pip',
    ensure   => '0.7',
    requires => Package['python-dev'],
  }

}
