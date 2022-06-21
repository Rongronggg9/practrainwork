(module
  (func (export "add_int") (param i32 i32) (result i32)
    local.get 0
    local.get 1
    i32.add)

  (func (export "sub_int") (param i32 i32) (result i32)
    local.get 0
    local.get 1
    i32.sub)

  (func (export "mul_int") (param i32 i32) (result i32)
    local.get 0
    local.get 1
    i32.mul)

  (func (export "div_int") (param i32 i32) (result i32)
    local.get 0
    local.get 1
    i32.div_s)

  (func (export "add_float") (param f64 f64) (result f64)
    local.get 0
    local.get 1
    f64.add)

  (func (export "sub_float") (param f64 f64) (result f64)
    local.get 0
    local.get 1
    f64.sub)

  (func (export "mul_float") (param f64 f64) (result f64)
    local.get 0
    local.get 1
    f64.mul)

  (func (export "div_float") (param f64 f64) (result f64)
    local.get 0
    local.get 1
    f64.div)
)
