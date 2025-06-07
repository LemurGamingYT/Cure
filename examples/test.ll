; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"snprintf"(i8* %".1", i64 %".2", i8* %".3", ...)

declare i32 @"puts"(i8* %".1")

declare void @"exit"(i32 %".1")

define i32 @"main"()
{
.2:
  %".3" = insertvalue {i8*, i64} undef, i8* getelementptr ([12 x i8], [12 x i8]* @"str", i32 0, i32 0), 0
  %".4" = insertvalue {i8*, i64} %".3", i64 11, 1
  %".5" = alloca {i8*, i64}
  store {i8*, i64} %".4", {i8*, i64}* %".5"
  %".7" = load {i8*, i64}, {i8*, i64}* %".5"
  %".8" = call i32 @"string_length"({i8*, i64} %".7")
  %".9" = call i8* @"print.1"(i32 %".8")
  ret i32 0
}

@"str" = internal constant [12 x i8] c"Hello world\00"
define i32 @"string_length"({i8*, i64} %".1")
{
.3:
  %".4" = extractvalue {i8*, i64} %".1", 1
  %".5" = trunc i64 %".4" to i32
  ret i32 %".5"
}

define i8* @"print.1"(i32 %".1")
{
.3:
  %".4" = call {i8*, i64} @"int_to_string"(i32 %".1")
  %".5" = extractvalue {i8*, i64} %".4", 0
  %".6" = call i32 @"puts"(i8* %".5")
  ret i8* null
}

define {i8*, i64} @"int_to_string"(i32 %".1")
{
.3:
  %".4" = call i32 (i8*, i64, i8*, ...) @"snprintf"(i8* getelementptr ([16 x i8], [16 x i8]* @".2", i32 0, i32 0), i64 16, i8* getelementptr ([3 x i8], [3 x i8]* @"str.1", i32 0, i32 0), i32 %".1")
  %".5" = insertvalue {i8*, i64} undef, i8* getelementptr ([16 x i8], [16 x i8]* @".2", i32 0, i32 0), 0
  %".6" = insertvalue {i8*, i64} %".5", i64 16, 1
  ret {i8*, i64} %".6"
}

@".2" = internal global [16 x i8] zeroinitializer
@"str.1" = internal constant [3 x i8] c"%d\00"