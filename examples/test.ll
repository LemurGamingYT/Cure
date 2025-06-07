; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"snprintf"(i8* %".1", i64 %".2", i8* %".3", ...)

declare i32 @"puts"(i8* %".1")

declare void @"exit"(i32 %".1")

define i32 @"main"()
{
.2:
  %".3" = call i8* @"print.1"(i1 true)
  ret i32 0
}

define i8* @"print.1"(i1 %".1")
{
.3:
  %".4" = call {i8*, i64} @"bool_to_string"(i1 %".1")
  %".5" = extractvalue {i8*, i64} %".4", 0
  %".6" = call i32 @"puts"(i8* %".5")
  ret i8* null
}

define {i8*, i64} @"bool_to_string"(i1 %".1")
{
.3:
  %".4" = select  i1 %".1", i8* getelementptr ([5 x i8], [5 x i8]* @"str", i32 0, i32 0), i8* getelementptr ([6 x i8], [6 x i8]* @"str.1", i32 0, i32 0)
  %".5" = select  i1 %".1", i64 4, i64 5
  %".6" = insertvalue {i8*, i64} undef, i8* %".4", 0
  %".7" = insertvalue {i8*, i64} %".6", i64 %".5", 1
  ret {i8*, i64} %".7"
}

@"str" = internal constant [5 x i8] c"true\00"
@"str.1" = internal constant [6 x i8] c"false\00"