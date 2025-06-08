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
  %"stdlib_call" = call {i8*, i64} @"string_new"(i8* getelementptr ([2 x i8], [2 x i8]* @"str", i32 0, i32 0), i32 1)
  %"stdlib_call.1" = call i8* @"print.1"({i8*, i64} %"stdlib_call")
  ret i32 0
}

@"str" = internal constant [2 x i8] c"H\00"
define {i8*, i64} @"string_new"(i8* %".1", i32 %".2")
{
.4:
  %".5" = zext i32 %".2" to i64
  %".6" = add i64 %".5", 1
  %".7" = call i8* @"malloc"(i64 %".6")
  %".8" = call i8* @"memcpy"(i8* %".7", i8* %".1", i64 %".5")
  %".9" = getelementptr i8, i8* %".7", i64 %".5"
  store i8 0, i8* %".9"
  %".11" = insertvalue {i8*, i64} undef, i8* %".7", 0
  %".12" = insertvalue {i8*, i64} %".11", i64 %".5", 1
  ret {i8*, i64} %".12"
}

define i8* @"print.1"({i8*, i64} %".1")
{
.3:
  %"stdlib_call" = call {i8*, i64} @"string_to_string"({i8*, i64} %".1")
  %".4" = extractvalue {i8*, i64} %"stdlib_call", 0
  %".5" = call i32 @"puts"(i8* %".4")
  ret i8* null
}

define {i8*, i64} @"string_to_string"({i8*, i64} %".1")
{
.3:
  ret {i8*, i64} %".1"
}
