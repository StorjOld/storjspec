# Bidirectional trustless micropayent channels

This is based on the worked previously done by the lightning network
developers. It is a simplified, less feature rich and should still meet all
our needs.

For more information on the underlying mechinisms see:

 * [BIP68](https://github.com/bitcoin/bips/blob/master/bip-0068.mediawiki)
 * [BIP112](https://github.com/bitcoin/bips/blob/master/bip-0112.mediawiki#Motivation)
 * [Lightning Network](https://lightning.network/lightning-network-paper.pdf)
 * [Deployable Lightning](https://github.com/ElementsProject/lightning/blob/master/doc/deployable-lightning.pdf)

![micropayment channel diagram](micropayments.png)


## Anchor transaction

The anchor transaction has two outputs, one for each party with the value of
the respective parties inputs.

At any time funds can be spent using signatures of both parties. This is used
to negotiate the symmetrical commit transactions.

After the channels expire time the owners can sign their output alone and
recover only their deposit with their respective recover keys.

If needed both parties can add additional funds to the payment channel by
sending funds to their respective outputs pay to script hash address.


Alice output script:

    OP_IF
        2 <alice pubkey> <bob pubkey> 2 OP_CHECKMULTISIGVERIFY
    OP_ELSE
        <expire time> OP_CHECKSEQUENCEVERIFY OP_DROP
        <alice recover pubkey> OP_CHECKSIGVERIFY
    OP_ENDIF


Bob output script:

    OP_IF
        2 <alice pubkey> <bob pubkey> 2 OP_CHECKMULTISIGVERIFY
    OP_ELSE
        <expire time> OP_CHECKSEQUENCEVERIFY OP_DROP
        <bob recover pubkey> OP_CHECKSIGVERIFY
    OP_ENDIF


## Commit transaction

Using the outputs of the anchor transacton both parties periodically
renegotiate a pair of symmetrical commit transactions that can be used to
close the payment channel. Both use the same inputs and transfer the same
amount to each party.

Whenever a new pair of commit transactions is negotiated, both parties
publish their revocation secret for the previous commit transaction. This
prevents the spending of the previous commit transactions.

Two commit transactions are required as both revocation secrets cannot be
published atomically at once. Publishing any one of the commit transactions
will close the payment channel. If both are published, it is a double spend
and only one will be accepted.


### Alice commit transaction

Alice output script:

    OP_HASH160 <alice revocation secret hash> OP_EQUAL
    OP_IF
        <bob pubkey>
    OP_ELSE
        <delay time> OP_CHECKSEQUENCEVERIFY OP_DROP
        <alice pubkey>
    OP_ENDIF
    OP_CHECKSIG

Bob output script

    <bob pubkey> OP_CHECKSIG


### Bob commit transaction

Alice output script

    <alice pubkey> OP_CHECKSIG

Bob output script:

    OP_HASH160 <bob revocation secret hash> OP_EQUAL
    OP_IF
        <alice pubkey>
    OP_ELSE
        <delay time> OP_CHECKSEQUENCEVERIFY OP_DROP
        <bob pubkey>
    OP_ENDIF
    OP_CHECKSIG

