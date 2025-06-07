; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"snprintf"(i8* %".1", i64 %".2", i8* %".3", ...)

declare i32 @"puts"(i8* %".1")

declare void @"exit"(i32 %".1")

define i32 @"main"()
{
.2:
  br label %"while_condition"
while_condition:
  br i1 true, label %"while_body", label %"while_exit"
while_body:
  %".5" = insertvalue {i8*, i64} undef, i8* getelementptr ([2 x i8], [2 x i8]* @"str", i32 0, i32 0), 0
  %".6" = insertvalue {i8*, i64} %".5", i64 1, 1
  %".7" = call i8* @"print.1"({i8*, i64} %".6")
  br label %"while_condition"
while_exit:
  %".9" = insertvalue {i8*, i64} undef, i8* getelementptr ([2 x i8], [2 x i8]* @"str.1", i32 0, i32 0), 0
  %".10" = insertvalue {i8*, i64} %".9", i64 1, 1
  %".11" = call i8* @"print.1"({i8*, i64} %".10")
  ret i32 0
}

@"str" = internal constant [2 x i8] c"A\00"
define i8* @"print.1"({i8*, i64} %".1")
{
.3:
  %".4" = call {i8*, i64} @"string_to_string"({i8*, i64} %".1")
  %".5" = extractvalue {i8*, i64} %".4", 0
  %".6" = call i32 @"puts"(i8* %".5")
  ret i8* null
}

define {i8*, i64} @"string_to_string"({i8*, i64} %".1")
{
.3:
  ret {i8*, i64} %".1"
}

@"str.1" = internal constant [2 x i8] c"A\00"