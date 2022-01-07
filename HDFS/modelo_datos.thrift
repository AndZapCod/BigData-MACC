################ Atomic data #####################

union ArtistID{
    1: string id;
}

union SongID{
    1: string id;
}

struct Location{
    1: optional string name;
    2: optional double latitude;
    3: optional double longitude;
}

union ArtistPropertyValue{
    1: string name;
    2: Location location;
}

union SongPropertyValue{
    1: string title;
    2: i32 duration;
}

struct Pedigree{
    1: required i32 year;
}

################# Properties #####################

struct ArtistProperty{
    1: required ArtistID id;
    2: required ArtistPropertyValue property;
}

struct SongProperty{
    1: required SongID id;
    2: required SongPropertyValue property;
}
################### Edges ########################

struct InterpretedByEdge{
    1: required ArtistID artist;
    2: required SongID song;
}

struct SimilarityEdge{
    1: required ArtistID artist1;
    2: required ArtistID artist2;
}


################# Data units #####################

union DataUnit{
    1: ArtistProperty person_property;
    2: SongProperty page_property;
    3: InterpretedByEdge inter;
    4: SimilarityEdge sim;
}

struct Data{
    1: required Pedigree pedigree;
    2: required DataUnit dataunit;
}