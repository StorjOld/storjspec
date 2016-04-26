# Bidirectional trustless micropayent channels

This is based on the worked previously done by the lightning network
developers. It is a simplified, less feature rich and should still meet all
our needs.

For more information on the underlying mechinisms see:

 * [BIP112](https://github.com/bitcoin/bips/blob/master/bip-0112.mediawiki#Motivation)
 * [BIP68](https://github.com/bitcoin/bips/blob/master/bip-0068.mediawiki)
 * [Deployable Lightning](https://github.com/ElementsProject/lightning/blob/master/doc/deployable-lightning.pdf)
 * [Lightning Network](https://lightning.network/lightning-network-paper.pdf)

![micropayment channel diagram](micropayments.png)


## Anchor

Script:

    IF
        2 <owner_pubkey> <counterparty_pubkey> 2 OP_CHECKMULTISIGVERIFY
    ELSE
        <expire_time> OP_CHECKSEQUENCEVERIFY OP_DROP
        <recover_pubkey> OP_CHECKSIGVERIFY
    ENDIF


## Commit

Owner output script:

    IF
        <delay> OP_CHECKSEQUENCEVERIFY OP_DROP <owner_pubkey> OP_CHECKSIG
    ELSE
        OP_HASH160 <revocation_secret_hash> OP_EQUALVERIFY
        OP_DROP <counterparty_pubkey> OP_CHECKSIG
    ENDIF

Counterparty output script

    <owner_pubkey> OP_CHECKSIG
