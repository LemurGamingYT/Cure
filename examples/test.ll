; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare external i32 @"snprintf"(i8* %".1", i64 %".2", i8* %".3", ...)

declare external i32 @"puts"(i8* %".1")

declare external void @"exit"(i32 %".1")

define i32 @"main"()
{
.2:
  %".3" = insertvalue {i8*, i64} undef, i8* getelementptr ([2 x i8], [2 x i8]* @"str", i32 0, i32 0), 0
  %".4" = insertvalue {i8*, i64} %".3", i64 1, 1
  %".5" = call i8* @"assert"(i1 false, {i8*, i64} %".4")
  ret i32 0
}

@"str" = internal constant [2 x i8] c"A\00"
define i8* @"assert"(i1 %".1", {i8*, i64} %".2")
{
.4:
  %".5" = xor i1 %".1", -1
  br i1 %".5", label %".4.if", label %".4.endif"
.4.if:
  %".7" = call i8* @"error"({i8*, i64} %".2")
  ret i8* null
.4.endif:
  ret i8* null
}

define i8* @"error"({i8*, i64} %".1")
{
.3:
  %".4" = extractvalue {i8*, i64} %".1", 0
  %".5" = call i32 @"puts"(i8* %".4")
  call void @"exit"(i32 1)
  ret i8* null
}
