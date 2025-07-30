from nf_common_base.b_source.common.configurations.b_clearer_configurations.b_clearer_domain_configurations import (
    BClearerDomainConfigurations,
)


# TODO: should we move BEnums() to nf_common? - MOVED
class BClearerDomainGraphConfigurations(
    BClearerDomainConfigurations
):
    SOURCE_GRAPH_FILE_FORMAT = str()
