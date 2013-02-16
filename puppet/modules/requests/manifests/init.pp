class requests {

  package { 'requests':
    provider => 'pip',
    ensure   => '1.1',
  }

}
