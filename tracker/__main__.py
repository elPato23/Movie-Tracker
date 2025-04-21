from tracker import TVShowAdapter, TelevisionDB


tv_adapter = TVShowAdapter(TelevisionDB())
trending = tv_adapter.search("How I Met your Mother")
for show in trending:
    print(show.name)
    print(show.description)
    print(
        "Total Seasons:", show.length.seasons, "Total Episodes:", show.length.episodes
    )
    print(show.genres)
    print(show.networks)
    print("--" * 20)
