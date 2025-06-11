; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare external i32 @"snprintf"(i8* %".1", i64 %".2", i8* %".3", ...)

declare external i32 @"puts"(i8* %".1")

declare external void @"exit"(i32 %".1")

declare external i8* @"malloc"(i64 %".1")

declare external void @"free"(i8* %".1")

declare external i8* @"memcpy"(i8* %".1", i8* %".2", i64 %".3")

define i32 @"test"(i32 %".1")
{
entry:
  %"stdlib_call" = call i32 @"int_add_int"(i32 %".1", i32 1)
  ret i32 %"stdlib_call"
}

define i32 @"int_add_int"(i32 %".1", i32 %".2")
{
.4:
  %".5" = add i32 %".1", %".2"
  ret i32 %".5"
}

define i32 @"main"()
{
entry:
  %"func_call" = call i32 @"test"(i32 10)
  %"stdlib_call" = call i8* @"print.1"(i32 %"func_call")
  ret i32 0
}

define i8* @"print.1"(i32 %".1")
{
.3:
  %"stdlib_call" = call {i8*, i64, {i8*, i8* (i8*)*, i64}*} @"int_to_string"(i32 %".1")
  %".4" = extractvalue {i8*, i64, {i8*, i8* (i8*)*, i64}*} %"stdlib_call", 0
  %".5" = call i32 @"puts"(i8* %".4")
  ret i8* null
}

define {i8*, i64, {i8*, i8* (i8*)*, i64}*} @"int_to_string"(i32 %".1")
{
.3:
  %".4" = call i32 (i8*, i64, i8*, ...) @"snprintf"(i8* getelementptr ([16 x i8], [16 x i8]* @".2", i32 0, i32 0), i64 16, i8* getelementptr ([3 x i8], [3 x i8]* @"str", i32 0, i32 0), i32 %".1")
  %".5" = trunc i64 16 to i32
  %"stdlib_call" = call {i8*, i64, {i8*, i8* (i8*)*, i64}*} @"string_new"(i8* getelementptr ([16 x i8], [16 x i8]* @".2", i32 0, i32 0), i32 %".5")
  ret {i8*, i64, {i8*, i8* (i8*)*, i64}*} %"stdlib_call"
}

@".2" = internal global [16 x i8] zeroinitializer
@"str" = internal constant [3 x i8] c"%d\00"
define {i8*, i64, {i8*, i8* (i8*)*, i64}*} @"string_new"(i8* %".1", i32 %".2")
{
.4:
  %".5" = zext i32 %".2" to i64
  %".6" = add i64 %".5", 1
  %".7" = call i8* @"malloc"(i64 %".6")
  %".8" = call i8* @"memcpy"(i8* %".7", i8* %".1", i64 %".5")
  %".9" = getelementptr i8, i8* %".7", i64 %".5"
  store i8 0, i8* %".9"
  %"stdlib_call" = call {i8*, i8* (i8*)*, i64}* @"Ref_new.3"(i8* %".7", i8* (i8*)* null)
  %".11" = insertvalue {i8*, i64, {i8*, i8* (i8*)*, i64}*} undef, i8* %".7", 0
  %".12" = insertvalue {i8*, i64, {i8*, i8* (i8*)*, i64}*} %".11", i64 %".5", 1
  %".13" = insertvalue {i8*, i64, {i8*, i8* (i8*)*, i64}*} %".12", {i8*, i8* (i8*)*, i64}* %"stdlib_call", 2
  ret {i8*, i64, {i8*, i8* (i8*)*, i64}*} %".13"
}

define {i8*, i8* (i8*)*, i64}* @"Ref_new.3"(i8* %".1", i8* (i8*)* %".2")
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
