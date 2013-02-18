import 'lib/*.pp'
import 'nodes/*.pp'

#
# Modules included for all nodes.
#
class common {

    include python
    include hotworker
    include git
    include fabric
    include curl
    include libncurses
    include libpcre
    include libreadline
    include libssl
    include perl
    include openresty
    include circus
    include redis
    include requests
    include flask
    include chaussette

}
