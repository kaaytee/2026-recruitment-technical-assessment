use axum::{http::StatusCode, response::IntoResponse, Json};
use serde::{Deserialize, Serialize};

pub enum Data {
    String(String),
    Integer(i32)
}

pub async fn process_data(Json(request): Json<DataRequest>) -> impl IntoResponse {
    // Calculate sums and return response

    let mut string_len = 0;
    let mut int_sum = 0;
    let response = DataResponse {
        for v in request.data {
            match v {
                Data::String(strr) =>  string_len + strr.len(),
                Data::Integer(int) => int_sum = int_sum +  intl,
                _ => (),
            }
        }



    };

    (StatusCode::OK, Json(response))
}

#[derive(Deserialize)]
pub struct DataRequest {
    pub data: Vec<Data>,
}

#[derive(Serialize)]
pub struct DataResponse {
    pub string_len: i32
    pub int_sum: i32
}
