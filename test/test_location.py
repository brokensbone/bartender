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