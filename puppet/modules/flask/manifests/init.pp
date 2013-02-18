class flask {

  package { 'flask':
    provider => 'pip',
    ensure   => '0.9',
    requires => Package['python-dev'],
  }

  package { 'flask-script':
    provider => 'pip',
    ensure   => '0.5.3',
    requires => Package['python-dev'],
  }

}
