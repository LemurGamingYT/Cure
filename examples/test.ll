; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"snprintf"(i8* %".1", i64 %".2", i8* %".3", ...)

declare i32 @"puts"(i8* %".1")

define i32 @"main"()
{
.2:
  %".3" = alloca i32
  store i32 20, i32* %".3"
  %".5" = load i32, i32* %".3"
  %".6" = call i8* @"print.1"(i32 %".5")
  store i32 10, i32* %".3"
  %".8" = load i32, i32* %".3"
  %".9" = call i8* @"print.1"(i32 %".8")
  ret i32 0
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
  %".4" = call i32 (i8*, i64, i8*, ...) @"snprintf"(i8* getelementptr ([16 x i8], [16 x i8]* @".2", i32 0, i32 0), i64 16, i8* getelementptr ([3 x i8], [3 x i8]* @"str", i32 0, i32 0), i32 %".1")
  %".5" = insertvalue {i8*, i64} undef, i8* getelementptr ([16 x i8], [16 x i8]* @".2", i32 0, i32 0), 0
  %".6" = insertvalue {i8*, i64} %".5", i64 16, 1
  ret {i8*, i64} %".6"
}

@".2" = internal global [16 x i8] zeroinitializer
@"str" = internal constant [3 x i8] c"%d\00"