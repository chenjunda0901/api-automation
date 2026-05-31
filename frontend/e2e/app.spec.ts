/**
 * Playwright E2E Tests - API Pilot
 * 端到端测试套件
 */
import { test, expect } from '@playwright/test'

// ============================================================
// 认证相关测试
// ============================================================
test.describe('Authentication', () => {
  test('should display login page', async ({ page }) => {
    await page.goto('/login')
    
    // 验证登录页面元素
    await expect(page.locator('h2, h3, .login-title')).toBeVisible()
    await expect(page.getByPlaceholder(/用户名|账号|account/i)).toBeVisible()
    await expect(page.getByPlaceholder(/密码|password/i)).toBeVisible()
  })

  test('should show validation errors for empty fields', async ({ page }) => {
    await page.goto('/login')
    
    // 点击登录按钮
    const loginButton = page.getByRole('button', { name: /登录|登录/i })
    if (await loginButton.isVisible()) {
      await loginButton.click()
      
      // 验证错误提示
      await expect(page.locator('.el-form-item__error, .error-message, [role="alert"]').first()).toBeVisible()
    }
  })

  test('should login successfully with valid credentials', async ({ page }) => {
    await page.goto('/login')
    
    // 填写登录信息
    const usernameInput = page.getByPlaceholder(/用户名|账号/i)
    const passwordInput = page.getByPlaceholder(/密码/i)
    
    if (await usernameInput.isVisible()) {
      await usernameInput.fill('admin')
      await passwordInput.fill('admin123')
      
      // 提交
      const loginButton = page.getByRole('button', { name: /登录/i })
      await loginButton.click()
      
      // 验证跳转
      await page.waitForURL(/projects|dashboard|home/i, { timeout: 10000 })
    }
  })
})

// ============================================================
// 导航相关测试
// ============================================================
test.describe('Navigation', () => {
  test.beforeEach(async ({ page }) => {
    // 尝试登录或跳过认证（根据实际情况调整）
    await page.goto('/')
    // 如果需要登录，可以在这里处理
  })

  test('should navigate to dashboard', async ({ page }) => {
    // 点击仪表盘链接
    const dashboardLink = page.locator('a[href="/"], .nav-item:has-text("仪表盘")').first()
    
    if (await dashboardLink.isVisible({ timeout: 5000 }).catch(() => false)) {
      await dashboardLink.click()
      await expect(page.locator('.page-title, h1')).toContainText(/仪表盘|dashboard/i)
    }
  })

  test('should navigate to projects', async ({ page }) => {
    // 点击项目管理链接
    const projectsLink = page.locator('a[href="/projects"], .nav-item:has-text("项目管理")').first()
    
    if (await projectsLink.isVisible({ timeout: 5000 }).catch(() => false)) {
      await projectsLink.click()
      await page.waitForURL(/\/projects/)
      await expect(page.locator('.page-title, h1')).toContainText(/项目|projects/i)
    }
  })
})

// ============================================================
// 项目管理测试
// ============================================================
test.describe('Projects Management', () => {
  test('should display projects list', async ({ page }) => {
    await page.goto('/projects')
    
    // 验证页面标题
    await expect(page.locator('.page-title, h1').first()).toBeVisible()
    
    // 验证创建项目按钮
    const createButton = page.getByRole('button', { name: /新建|创建|新增/i })
    await expect(createButton).toBeVisible()
  })

  test('should open create project dialog', async ({ page }) => {
    await page.goto('/projects')
    
    // 点击新建项目按钮
    const createButton = page.getByRole('button', { name: /新建|创建|新增/i })
    await createButton.click()
    
    // 验证对话框
    const dialog = page.locator('.el-dialog, [role="dialog"], .modal')
    await expect(dialog).toBeVisible()
    
    // 验证表单字段
    await expect(page.getByLabel(/项目名称|name/i).or(page.getByPlaceholder(/项目名称/i))).toBeVisible()
  })

  test('should create a new project', async ({ page }) => {
    await page.goto('/projects')
    
    // 打开创建对话框
    const createButton = page.getByRole('button', { name: /新建|创建/i })
    await createButton.click()
    
    // 填写项目名称
    const nameInput = page.getByPlaceholder(/请输入项目名称/i)
    if (await nameInput.isVisible({ timeout: 3000 }).catch(() => false)) {
      const projectName = `Test Project ${Date.now()}`
      await nameInput.fill(projectName)
      
      // 提交
      const submitButton = page.getByRole('button', { name: /确定|创建/i })
      await submitButton.click()
      
      // 验证项目创建成功
      await expect(page.locator('.project-name, .project-card').first()).toBeVisible()
    }
  })
})

// ============================================================
// 主题切换测试
// ============================================================
test.describe('Theme Switching', () => {
  test('should display theme switcher', async ({ page }) => {
    await page.goto('/')
    
    // 等待页面加载
    await page.waitForLoadState('networkidle')
    
    // 查找主题切换器
    const themeSwitcher = page.locator('.theme-switcher').first()
    await expect(themeSwitcher).toBeVisible()
  })

  test('should switch theme options', async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')
    
    // 点击主题切换器
    const themeSwitcher = page.locator('.theme-switcher').first()
    await themeSwitcher.click()
    
    // 验证下拉菜单
    const dropdown = page.locator('.theme-menu, .el-dropdown-menu').first()
    await expect(dropdown).toBeVisible()
    
    // 验证主题选项
    await expect(page.locator('text=深色')).toBeVisible()
    await expect(page.locator('text=浅色')).toBeVisible()
    await expect(page.locator('text=跟随系统')).toBeVisible()
  })

  test('should apply dark theme', async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')
    
    // 切换到深色主题
    const themeSwitcher = page.locator('.theme-switcher').first()
    await themeSwitcher.click()
    
    const darkOption = page.locator('.el-dropdown-menu__item:has-text("深色")').first()
    await darkOption.click()
    
    // 验证主题属性
    const html = page.locator('html')
    await expect(html).toHaveAttribute('data-theme', 'dark')
  })

  test('should apply light theme', async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')
    
    // 切换到浅色主题
    const themeSwitcher = page.locator('.theme-switcher').first()
    await themeSwitcher.click()
    
    const lightOption = page.locator('.el-dropdown-menu__item:has-text("浅色")').first()
    await lightOption.click()
    
    // 验证主题属性
    const html = page.locator('html')
    await expect(html).toHaveAttribute('data-theme', 'light')
  })
})

// ============================================================
// 响应式测试
// ============================================================
test.describe('Responsive Design', () => {
  const viewports = [
    { name: 'mobile', width: 375, height: 667 },
    { name: 'tablet', width: 768, height: 1024 },
    { name: 'desktop', width: 1920, height: 1080 },
  ]

  for (const viewport of viewports) {
    test(`should render correctly on ${viewport.name}`, async ({ page }) => {
      await page.setViewportSize({ width: viewport.width, height: viewport.height })
      await page.goto('/')
      
      // 验证基本元素可见
      await expect(page.locator('.app-layout, .sidebar, .main-content').first()).toBeVisible()
      
      // 验证内容区域
      await expect(page.locator('.content-area, .topbar').first()).toBeVisible()
    })
  }
})

// ============================================================
// 性能相关测试
// ============================================================
test.describe('Performance', () => {
  test('should load page within acceptable time', async ({ page }) => {
    const startTime = Date.now()
    
    await page.goto('/')
    await page.waitForLoadState('networkidle')
    
    const loadTime = Date.now() - startTime
    
    // 验证加载时间在可接受范围内（3秒）
    expect(loadTime).toBeLessThan(3000)
  })

  test('should not have console errors', async ({ page }) => {
    const errors: string[] = []
    
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        errors.push(msg.text())
      }
    })
    
    await page.goto('/')
    await page.waitForLoadState('networkidle')
    
    // 过滤掉无关紧要的错误（如第三方库）
    const criticalErrors = errors.filter(err => 
      !err.includes('favicon') && 
      !err.includes('chunk') &&
      !err.includes('DevTools')
    )
    
    expect(criticalErrors).toHaveLength(0)
  })
})