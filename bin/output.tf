##########################################################
# output 
##########################################################

# VERFICATION
output "application" {
  value = "${data.external.tagging.result["application"]}"
}
output "deploymentId" {
  value = "${data.external.tagging.result["deploymentId"]}"
}
output "done" {
  value = 0
  depends_on = [
    aws_dynamodb_table.dyn_state,
    aws_s3_bucket.s3_state
  ]
}

# RESOURCE SPECFIC 
output "admin-user_key" {
  value = "${aws_iam_access_key.admin-user.id}"
}
output "admin-user_secret" {
  value     = "${aws_iam_access_key.admin-user.secret}"
  sensitive = true
}
output "read-user_key" {
  value = "${aws_iam_access_key.read-user.id}"
}
output "read-user_secret" {
  value     = "${aws_iam_access_key.read-user.secret}"
  sensitive = true
}


