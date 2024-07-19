import request from "@/utils/request";


export function getAdv() {
  return request({
    url: "/advertisers/getAdv",
    method: "get",
  });
}

export function like(id) {
  return request({
    url: "/users/like",
    method: "post",
    data: {
      ads_id: id
    }
  });
}

export function dislike(id) {
  return request({
    url: "/users/dislike",
    method: "post",
    data: {
      ads_id: id
    }
  });
}

export function dragAndDrop(idArray) {
  return request({
    url: "/users/dragAndDrop",
    method: "post",
    data: {
      ads_id_list: idArray
    }
  })
}
