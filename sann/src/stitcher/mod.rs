mod greedy;
mod smart;
pub mod types;



use graph::types::{ThickSurface, INNER, OUTER};



pub fn stitch_choice(ts: &ThickSurface, strategy: types::Strategy) -> types::Stitching {
    match strategy {
        types::Strategy::Dijkstra => smart::stitch(&ts.layers[OUTER], &ts.layers[INNER]),
        types::Strategy::Greedy => greedy::stitch(&ts.layers[OUTER], &ts.layers[INNER]),
    }
}

pub fn stitch_default(ts: &ThickSurface) -> types::Stitching {
    stitch_choice(ts, types::Strategy::Dijkstra)
}
