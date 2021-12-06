from src import provider



def test_location_backend(application):
    loc = provider.location_manager()

    r = loc.retrieve_location(12345)
    assert r is None

    longitude = 53.4814467
    latitude = -2.2500729
    name = "A bench in Manchester"

    loc.new_location(longitude, latitude, name)

    vs = loc.get_venues_near(longitude+0.2, latitude+0.2)
    assert len(vs) == 0

    vs = loc.get_venues_near(longitude+0.05, latitude+0.05)
    assert len(vs) > 0

    by_name = {v.name : v for v in vs}
    v = by_name[name]

    v2 = loc.retrieve_location(v.rowid)
    assert v.rowid == v2.rowid
    assert v.longitude == v2.longitude
    assert v.latitude == v2.latitude

    updated_name = "A really nice bench in Manchester"
    v2.name = updated_name
    loc.update_location(v2)

    v3 = loc.retrieve_location(v2.rowid)
    assert v3.name == updated_name


def test_location_frontend(client, authentication_headers):
    loc = provider.location_manager()

    r = client.get("location/12345", headers=authentication_headers)
    assert r.status_code == 404

    r = client.post("location/12345", headers=authentication_headers, json={"key":"value"})
    assert r.status_code == 404

    longitude = 53.47797644414097 
    latitude = -2.25236180482156
    name = "A park in Manchester"

    json_data = {"data": {"longitude":longitude, "latitude":latitude, "name":name}}
    client.post("location/new", json=json_data, headers=authentication_headers)
    
    query = {"longitude" : longitude+0.2, "latitude": latitude+0.2}
    r = client.get("location/search", query_string=query, headers=authentication_headers)
    names = [j["name"] for j in r.get_json()["data"]]
    assert name not in names
    
    query = {"longitude" : longitude+0.05, "latitude": latitude+0.05}
    r = client.get("location/search", query_string=query, headers=authentication_headers)
    vs = r.get_json()["data"]
    names = [j["name"] for j in vs]
    assert name in names
    

    by_name = {v["name"] : v for v in vs}
    v = by_name[name]

    location_id_url = "location/{}".format(v["rowid"])
    r = client.get(location_id_url, headers=authentication_headers)
    v2 = r.get_json()["data"]
    assert v["rowid"] == v2["rowid"]
    assert v["longitude"] == v2["longitude"]
    assert v["latitude"] == v2["latitude"]

    updated_name = "A really nice bench in Manchester"
    v2["name"] = updated_name
    r = client.post(location_id_url, headers=authentication_headers, json=v2)

    r = client.get(location_id_url, headers=authentication_headers)
    v3 = r.get_json()["data"]
    assert v3["name"] == updated_name