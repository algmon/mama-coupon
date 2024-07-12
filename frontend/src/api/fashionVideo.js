import request from "@/utils/request";

export function getAdv() {
  return request({
    url: "/advertisers/getAdv",
    method: "get",
  });
}
