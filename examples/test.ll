; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"snprintf"(i8* %".1", i64 %".2", i8* %".3", ...)

declare i32 @"puts"(i8* %".1")

declare void @"exit"(i32 %".1")

define i32 @"fact"(i32 %".1")
{
.3:
  %".4" = call i1 @"int_lte_int"(i32 %".1", i32 1)
  br i1 %".4", label %"if_then", label %"if_merge"
if_merge:
  %".7" = call i32 @"int_sub_int"(i32 %".1", i32 1)
  %".8" = call i32 @"fact"(i32 %".7")
  %".9" = call i32 @"int_mul_int"(i32 %".1", i32 %".8")
  ret i32 %".9"
if_then:
  ret i32 1
}

define i1 @"int_lte_int"(i32 %".1", i32 %".2")
{
.4:
  %".5" = icmp sle i32 %".1", %".2"
  ret i1 %".5"
}

define i32 @"int_sub_int"(i32 %".1", i32 %".2")
{
.4:
  %".5" = call {i32, i1} @"llvm.ssub.with.overflow.i32"(i32 %".1", i32 %".2")
  %".6" = extractvalue {i32, i1} %".5", 0
  %".7" = extractvalue {i32, i1} %".5", 1
  br i1 %".7", label %"underflow", label %".8"
underflow:
  %".10" = insertvalue {i8*, i64} undef, i8* getelementptr ([18 x i8], [18 x i8]* @"str", i32 0, i32 0), 0
  %".11" = insertvalue {i8*, i64} %".10", i64 17, 1
  %".12" = call i8* @"error"({i8*, i64} %".11")
  ret i32 0
.8:
  ret i32 %".6"
}

declare {i32, i1} @"llvm.ssub.with.overflow.i32"(i32 %".1", i32 %".2")

@"str" = internal constant [18 x i8] c"integer underflow\00"
define i8* @"error"({i8*, i64} %".1")
{
.3:
  %".4" = extractvalue {i8*, i64} %".1", 0
  %".5" = call i32 @"puts"(i8* %".4")
  call void @"exit"(i32 1)
  ret i8* null
}

define i32 @"int_mul_int"(i32 %".1", i32 %".2")
{
.4:
  %".5" = call {i32, i1} @"llvm.smul.with.overflow.i32"(i32 %".1", i32 %".2")
  %".6" = extractvalue {i32, i1} %".5", 0
  %".7" = extractvalue {i32, i1} %".5", 1
  br i1 %".7", label %"overflow", label %".8"
overflow:
  %".10" = insertvalue {i8*, i64} undef, i8* getelementptr ([17 x i8], [17 x i8]* @"str.1", i32 0, i32 0), 0
  %".11" = insertvalue {i8*, i64} %".10", i64 16, 1
  %".12" = call i8* @"error"({i8*, i64} %".11")
  ret i32 0
.8:
  ret i32 %".6"
}

declare {i32, i1} @"llvm.smul.with.overflow.i32"(i32 %".1", i32 %".2")

@"str.1" = internal constant [17 x i8] c"integer overflow\00"
define i32 @"main"()
{
.2:
  %".3" = call i32 @"fact"(i32 5)
  %".4" = call i8* @"print.1"(i32 %".3")
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
  %".4" = call i32 (i8*, i64, i8*, ...) @"snprintf"(i8* getelementptr ([16 x i8], [16 x i8]* @".2", i32 0, i32 0), i64 16, i8* getelementptr ([3 x i8], [3 x i8]* @"str.2", i32 0, i32 0), i32 %".1")
  %".5" = insertvalue {i8*, i64} undef, i8* getelementptr ([16 x i8], [16 x i8]* @".2", i32 0, i32 0), 0
  %".6" = insertvalue {i8*, i64} %".5", i64 16, 1
  ret {i8*, i64} %".6"
}

@".2" = internal global [16 x i8] zeroinitializer
@"str.2" = internal constant [3 x i8] c"%d\00"