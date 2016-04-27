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

After the channels expire time the owners can sign alone and recover their
deposit with their respective recover keys.


Output script:

    OP_IF
        2 <pubkey> <pubkey> 2 OP_CHECKMULTISIGVERIFY
    OP_ELSE
        <expire time> OP_CHECKSEQUENCEVERIFY OP_DROP
        <recover pubkey> OP_CHECKSIGVERIFY
    OP_ENDIF


## Commit transaction

Owner output script:

    OP_HASH160 <revocation secret hash> OP_EQUAL
    OP_IF
        <counterparty pubkey>
    OP_ELSE
        <delay time> OP_CHECKSEQUENCEVERIFY OP_DROP
        <owner pubkey>
    OP_ENDIF
    OP_CHECKSIG

This allows the owner to publish its latest commit transaction at any time
and spend the funds after a delay, but also ensures that if the owner relays
a revoked transaction, the counterparty has the delay time to claim the funds.

Counterparty output script

    <owner pubkey> OP_CHECKSIG
