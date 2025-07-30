from nf_common_base.b_source.common.configurations.b_clearer_configurations.b_clearer_configurations import (
    BClearerConfigurations,
)


class BieConfigurations(
    BClearerConfigurations
):
    ENABLE_BIE_UNIVERSE_INSPECTION = (
        True
    )

    B_SEQUENCE_NAME_TRUNCATION_LEVEL = 0
    #
    # DEFAULT_DIGEST_SIZE = \
    #     8
