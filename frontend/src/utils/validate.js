// 手机号校验
export function validatePhone(rule, value, callback) {
  if (!value) {
    callback()
    return
  }
  const reg = /^1[3-9]\d{9}$/
  if (reg.test(value)) {
    callback()
  } else {
    callback(new Error('请输入正确的手机号'))
  }
}

// 邮箱校验
export function validateEmail(rule, value, callback) {
  if (!value) {
    callback()
    return
  }
  const reg = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (reg.test(value)) {
    callback()
  } else {
    callback(new Error('请输入正确的邮箱地址'))
  }
}

// 确认密码校验
export function validateConfirmPassword(getPassword) {
  return (rule, value, callback) => {
    if (!value) {
      callback(new Error('请再次输入密码'))
    } else if (value !== getPassword()) {
      callback(new Error('两次输入密码不一致'))
    } else {
      callback()
    }
  }
}
