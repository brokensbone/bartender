
def test_api(client, authentication_headers):

    r = client.get("drink/beer/12345676", headers=authentication_headers)
    assert r.status_code == 404

    beer_data = {
        "brewery"   : "Hipster Brew Co.",
        "name"      : "Tasty Beer",
        "category"  : "IPA",
        "style"     : "NEIPA",
        "alcohol"   : 6.2,
        "notes"     : "Really nice!"
    }

    r = client.post("drink/beer/new", json=beer_data, headers=authentication_headers)
    assert r.status_code == 200
    rj = r.get_json()
    insert_id = rj["rowid"]

    r = client.get(f"drink/beer/{insert_id}", headers=authentication_headers)
    rj = r.get_json()["data"]
    assert rj["name"] == beer_data["name"]

    new_style = "West Coast IPA"
    new_alc = 5.4
    rj["style"] = new_style
    rj["alcohol"] = new_alc

    r = client.post(f"drink/beer/{insert_id}", json=rj, headers=authentication_headers)
    assert r.status_code == 200

    r = client.get(f"drink/beer/{insert_id}", headers=authentication_headers)
    rj = r.get_json()["data"]
    assert rj["style"] == new_style
    assert rj["alcohol"] == new_alc

    bad_dict = dict(beer_data)
    bad_dict.pop("name")
    r = client.post("drink/beer/new", json=bad_dict, headers=authentication_headers)
    assert r.status_code == 401

    r = client.post(f"drink/beer/{insert_id}", json=bad_dict, headers=authentication_headers)
    assert r.status_code == 401