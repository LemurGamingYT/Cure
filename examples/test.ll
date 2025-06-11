; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare external i32 @"snprintf"(i8* %".1", i64 %".2", i8* %".3", ...)

declare external i32 @"puts"(i8* %".1")

declare external void @"exit"(i32 %".1")

declare external i8* @"malloc"(i64 %".1")

declare external void @"free"(i8* %".1")

declare external i8* @"memcpy"(i8* %".1", i8* %".2", i64 %".3")

define i32 @"main"()
{
entry:
  %"stdlib_call" = call {i8*, i64, {i8*, i8* (i8*)*, i64}*} @"string_new"(i8* getelementptr ([12 x i8], [12 x i8]* @"str", i32 0, i32 0), i32 11)
  %".2" = alloca {i8*, i64, {i8*, i8* (i8*)*, i64}*}
  store {i8*, i64, {i8*, i8* (i8*)*, i64}*} %"stdlib_call", {i8*, i64, {i8*, i8* (i8*)*, i64}*}* %".2"
  %".4" = load {i8*, i64, {i8*, i8* (i8*)*, i64}*}, {i8*, i64, {i8*, i8* (i8*)*, i64}*}* %".2"
  %"stdlib_call.1" = call i8* @"print.2"({i8*, i64, {i8*, i8* (i8*)*, i64}*} %".4")
  %"stdlib_call.2" = call i8* @"string_destroy"({i8*, i64, {i8*, i8* (i8*)*, i64}*}* %".2")
  ret i32 0
}

@"str" = internal constant [12 x i8] c"Hello world\00"
define {i8*, i64, {i8*, i8* (i8*)*, i64}*} @"string_new"(i8* %".1", i32 %".2")
{
.4:
  %".5" = zext i32 %".2" to i64
  %".6" = add i64 %".5", 1
  %".7" = call i8* @"malloc"(i64 %".6")
  %".8" = call i8* @"memcpy"(i8* %".7", i8* %".1", i64 %".5")
  %".9" = getelementptr i8, i8* %".7", i64 %".5"
  store i8 0, i8* %".9"
  %"stdlib_call" = call {i8*, i8* (i8*)*, i64}* @"Ref_new.1"(i8* %".7", i8* (i8*)* null)
  %".11" = insertvalue {i8*, i64, {i8*, i8* (i8*)*, i64}*} undef, i8* %".7", 0
  %".12" = insertvalue {i8*, i64, {i8*, i8* (i8*)*, i64}*} %".11", i64 %".5", 1
  %".13" = insertvalue {i8*, i64, {i8*, i8* (i8*)*, i64}*} %".12", {i8*, i8* (i8*)*, i64}* %"stdlib_call", 2
  ret {i8*, i64, {i8*, i8* (i8*)*, i64}*} %".13"
}

define {i8*, i8* (i8*)*, i64}* @"Ref_new.1"(i8* %".1", i8* (i8*)* %".2")
{
.4:
  %".5" = getelementptr {i8*, i8* (i8*)*, i64}, {i8*, i8* (i8*)*, i64}* null, i32 1
  %".6" = ptrtoint {i8*, i8* (i8*)*, i64}* %".5" to i64
  %".7" = call i8* @"malloc"(i64 %".6")
  %".8" = bitcast i8* %".7" to {i8*, i8* (i8*)*, i64}*
  %".9" = getelementptr {i8*, i8* (i8*)*, i64}, {i8*, i8* (i8*)*, i64}* %".8", i32 0, i32 0
  store i8* %".1", i8** %".9"
  %".11" = getelementptr {i8*, i8* (i8*)*, i64}, {i8*, i8* (i8*)*, i64}* %".8", i32 0, i32 1
  store i8* (i8*)* %".2", i8* (i8*)** %".11"
  %".13" = getelementptr {i8*, i8* (i8*)*, i64}, {i8*, i8* (i8*)*, i64}* %".8", i32 0, i32 2
  store i64 1, i64* %".13"
  ret {i8*, i8* (i8*)*, i64}* %".8"
}

define i8* @"print.2"({i8*, i64, {i8*, i8* (i8*)*, i64}*} %".1")
{
.3:
  %"stdlib_call" = call {i8*, i64, {i8*, i8* (i8*)*, i64}*} @"string_to_string"({i8*, i64, {i8*, i8* (i8*)*, i64}*} %".1")
  %".4" = extractvalue {i8*, i64, {i8*, i8* (i8*)*, i64}*} %"stdlib_call", 0
  %".5" = call i32 @"puts"(i8* %".4")
  ret i8* null
}

define {i8*, i64, {i8*, i8* (i8*)*, i64}*} @"string_to_string"({i8*, i64, {i8*, i8* (i8*)*, i64}*} %".1")
{
.3:
  ret {i8*, i64, {i8*, i8* (i8*)*, i64}*} %".1"
}

define i8* @"string_destroy"({i8*, i64, {i8*, i8* (i8*)*, i64}*}* %".1")
{
.3:
  %".4" = getelementptr {i8*, i64, {i8*, i8* (i8*)*, i64}*}, {i8*, i64, {i8*, i8* (i8*)*, i64}*}* %".1", i32 0, i32 2
  %".5" = load {i8*, i8* (i8*)*, i64}*, {i8*, i8* (i8*)*, i64}** %".4"
  %"stdlib_call" = call i8* @"Ref_dec"({i8*, i8* (i8*)*, i64}* %".5")
  ret i8* null
}

define i8* @"Ref_dec"({i8*, i8* (i8*)*, i64}* %".1")
{
.3:
  %".4" = getelementptr {i8*, i8* (i8*)*, i64}, {i8*, i8* (i8*)*, i64}* %".1", i32 0, i32 2
  %".5" = load i64, i64* %".4"
  %".6" = sub i64 %".5", 1
  store i64 %".6", i64* %".4"
  %".8" = icmp eq i64 %".6", 0
  br i1 %".8", label %".3.if", label %".3.endif"
.3.if:
  %".10" = getelementptr {i8*, i8* (i8*)*, i64}, {i8*, i8* (i8*)*, i64}* %".1", i32 0, i32 0
  %".11" = load i8*, i8** %".10"
  %".12" = getelementptr {i8*, i8* (i8*)*, i64}, {i8*, i8* (i8*)*, i64}* %".1", i32 0, i32 1
  %".13" = load i8* (i8*)*, i8* (i8*)** %".12"
  %".14" = icmp ne i8* (i8*)* %".13", null
  br i1 %".14", label %".3.if.if", label %".3.if.else"
.3.endif:
  ret i8* null
.3.if.if:
  %".16" = call i8* %".13"(i8* %".11")
  br label %".3.if.endif"
.3.if.else:
  call void @"free"(i8* %".11")
  br label %".3.if.endif"
.3.if.endif:
  %".20" = bitcast {i8*, i8* (i8*)*, i64}* %".1" to i8*
  call void @"free"(i8* %".20")
  br label %".3.endif"
}
