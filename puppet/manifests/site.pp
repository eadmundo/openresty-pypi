import 'lib/*.pp'
import 'nodes/*.pp'

#
# Modules included for all nodes.
#
class common {

    #include python
    #include fabric
    #include git
    #include curl
    include libncurses
    include libpcre
    include libreadline
    include libssl
    include perl

}
