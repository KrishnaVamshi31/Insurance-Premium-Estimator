from app import UserInfo


def test_city_is_normalized_case_insensitively():
    data = UserInfo(
        age=35,
        weight=70,
        height=1.7,
        income_lpa=12,
        smoker=False,
        city="mumbai",
        occupation="private_job",
    )

    assert data.city == "Mumbai"
    assert data.city_tier == 1
