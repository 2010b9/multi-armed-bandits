import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Optional


def chose_arms_randomly(
    clients: List[int],
    arms: List[int]
) -> List[int]:
    """Choose an arm for each client uniformly at random"""

    return np.random.choice(arms, len(clients), replace=True)


def create_markings_dataset(
    clients: List[int],
    arms_for_each_client: List[int],
    date: Optional[datetime.date] = None
) -> pd.DataFrame:
    """Create a dataset with the client, date and associated arm"""

    data = pd.DataFrame(
        {
            "client_id": clients,
            "arm_id": arms_for_each_client
        }
    )

    if date is not None:
        data["date"] = date
        data["date"] = data["date"].astype("datetime64[ns]")

    return data


def generate_clients_ad_show(
    clients: List[int],
    n_samples: int,
    df_markings: pd.DataFrame,
    date: datetime.date
) -> List[int]:
    """Simulate the clients that have been shown an ad"""
    # Clients that are shown an add (they might click it or not)
    clients_ad_shown = np.random.choice(
        clients, size=n_samples, replace=False
    )

    df_clients_ad_shown = pd.DataFrame(
        {"client_id": clients_ad_shown, "date": date}
    )
    # Cast to datetime
    df_clients_ad_shown["date"] = df_clients_ad_shown[
        "date"
    ].astype("datetime64[ns]")

    return df_clients_ad_shown.merge(
        df_markings,
        how="inner",
        on=["date", "client_id"]
    ).sort_values("arm_id")


def create_clicks_dataset(
    df: List[int],
    probs: List[float]
) -> pd.DataFrame:
    """Create a dataset with the client, date, associated arm
    and if clicked or not"""

    ads_shown_count = df.value_counts("arm_id").sort_index()
    # Which ads were shown (it might be the case some of them are not shown)
    ads_shown = ads_shown_count.index.values
    # How many times each add was shown
    ads_count = ads_shown_count.values

    day_clicks = [
        np.random.binomial(
            1,  # Binary outcome (0 or 1)
            probs[ad],  # Probability of success
            count  # Sample size
        )
        for ad, count in zip(ads_shown, ads_count)
    ]
    day_clicks_flattened = np.hstack(day_clicks)

    df_copy = df.copy()
    df_copy["clicked"] = day_clicks_flattened

    return df_copy


def get_recommended_arms(
    df: pd.DataFrame,
    arms: List[int],
    n_clients: int
) -> List[int]:
    """Get probabilities of clicking each ad for each client"""

    # Number of users which have seen the ad and clicked
    numbers_of_rewards_1 =\
        df[df.clicked == 1].value_counts("arm_id").sort_index().to_dict()
    # Number of users which have seen the ad but have NOT clicked
    numbers_of_rewards_0 =\
        df[df.clicked == 0].value_counts("arm_id").sort_index().to_dict()

    beta_values = []
    for ad_id in arms:
        if ad_id not in numbers_of_rewards_1.keys():
            random_beta = np.array([0]*n_clients)
        else:
            a = numbers_of_rewards_1[ad_id] + 1
            b = numbers_of_rewards_0[ad_id] + 1
            random_beta = np.random.beta(a, b, n_clients)

        beta_values.append(random_beta)

    processed_array = np.transpose(np.vstack(beta_values))
    return [np.argmax(processed_array[i]) for i in range(n_clients)]


if __name__ == "__main__":
    # 5 different ads – with prob of being seen
    PROBS = [0.7112, 0.7113, 0.7113, 0.7115, 0.7116,
             0.7117, 0.7117, 0.7118, 0.7119, 0.7151]
    # probs = [0.1, 0.3, 0.4, 0.6, 0.7, 0.7117, 0.7117, 0.7118, 0.7119, 0.7221]
    ARMS = [i for i in range(len(PROBS))]
    N_CLIENTS = 100_000
    CLIENTS = [i for i in range(N_CLIENTS)]
    DATE = datetime(2023, 3, 2)

    arms_for_each_client = chose_arms_randomly(
        CLIENTS, ARMS
    )

    df_markings = create_markings_dataset(
        CLIENTS, arms_for_each_client, DATE.date()
    )

    clients_clicks = generate_clients_ad_show(
        CLIENTS,
        np.random.randint(10_000, 20_000),
        df_markings,
        DATE.date()
    )

    df_history = create_clicks_dataset(
        clients_clicks, PROBS
    )

    recommended_arms = get_recommended_arms(
        df_history, ARMS, N_CLIENTS
    )

    print(pd.DataFrame(recommended_arms).value_counts())
