import numpy as np



def normalize_scores(scores):


    values = np.array(
        list(scores.values())
    )


    max_value = values.max()


    if max_value == 0:

        return {
            key:0.0
            for key in scores
        }



    return {

        key:value/max_value

        for key,value
        in scores.items()

    }