; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"snprintf"(i8* %".1", i64 %".2", i8* %".3", ...)

declare i32 @"puts"(i8* %".1")

declare void @"exit"(i32 %".1")

define i32 @"main"()
{
.2:
  %".3" = call i8* @"print.1"(float 0x4034333340000000)
  ret i32 0
}

define i8* @"print.1"(float %".1")
{
.3:
  %".4" = call {i8*, i64} @"float_to_string"(float %".1")
  %".5" = extractvalue {i8*, i64} %".4", 0
  %".6" = call i32 @"puts"(i8* %".5")
  ret i8* null
}

define {i8*, i64} @"float_to_string"(float %".1")
{
.3:
  %".4" = fpext float %".1" to double
  %".5" = call i32 (i8*, i64, i8*, ...) @"snprintf"(i8* getelementptr ([64 x i8], [64 x i8]* @".2", i32 0, i32 0), i64 64, i8* getelementptr ([3 x i8], [3 x i8]* @"str", i32 0, i32 0), double %".4")
  %".6" = insertvalue {i8*, i64} undef, i8* getelementptr ([64 x i8], [64 x i8]* @".2", i32 0, i32 0), 0
  %".7" = insertvalue {i8*, i64} %".6", i64 64, 1
  ret {i8*, i64} %".7"
}

@".2" = internal global [64 x i8] zeroinitializer
@"str" = internal constant [3 x i8] c"%f\00"