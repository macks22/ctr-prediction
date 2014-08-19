# File descriptions

*   train.csv - The training set consists of a portion of Criteo's traffic over
    a period of 7 days. Each row corresponds to a display ad served by Criteo.
    Positive (clicked) and negatives (non-clicked) examples have both been
    subsampled at different rates in order to reduce the dataset size. The
    examples are chronologically ordered.

*   test.csv - The test set is computed in the same way as the training set but
    for events on the day following the training period.

# Feature Descriptions

There are 45840617 training instances.

*   Label - Target variable that indicates if an ad was clicked (1) or not (0).
*   I1-I13 - A total of 13 columns of integer features (mostly count features).
*   C1-C26 - A total of 26 columns of categorical features. The values of these
    features have been hashed onto 32 bits for anonymization purposes.

The semantic of the features is undisclosed.

When a value is missing, the field is empty.

## Feature Semantics

We are not disclosing the semantics of the features, but I can tell you that they
fall in the following categories:

*   Publisher features, such as the domain of the url where the ad was displayed;
*   Advertiser features (advertiser id, type of products,...)
*   User features, for instance browser type;
*   Interaction of the user with the advertiser, such as the number of the times the
    user visited the advertiser website.
