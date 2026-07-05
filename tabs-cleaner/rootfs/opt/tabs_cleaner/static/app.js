const DEFAULT_LOCALE = "zh-CN";
const LOCALE_STORAGE_KEY = "tabs-cleaner-language";
const CATALOGS = {
  "zh-CN": {
    "app.title": "TabS Cleaner",
    "language.label": "语言",
    "nav.smart": "智能清理",
    "nav.strategy": "清理策略",
    "nav.storage": "存储分布",
    "nav.docker": "Docker 系统",
    "nav.deep": "深度清理",
    "nav.history": "历史记录",
    "hero.eyebrow": "Home Assistant OS 存储养护",
    "hero.title": "为 HAOS 提供智能存储清理。",
    "button.scan": "扫描",
    "button.scanning": "扫描中...",
    "button.safeClean": "安全清理",
    "button.cleaning": "清理中...",
    "button.deepClean": "运行所选深度清理",
    "button.running": "运行中...",
    "status.notScanned": "尚未扫描",
    "status.unknown": "未知",
    "status.clean": "正常",
    "status.issueCount": "{count} 个问题",
    "metric.used": "已用",
    "metric.free": "可用",
    "metric.total": "总量",
    "smart.readyTitle": "准备扫描",
    "smart.readyDescription": "TabS Cleaner 会先检查 Docker 缓存、加载项数据、备份、日志和 HAOS 健康状态，再执行任何清理。",
    "smart.immediateTitle": "建议立即清理",
    "smart.scanCompleteTitle": "存储扫描完成",
    "smart.scanDescription": "最大类别：{category}。请先查看安全清理，再按需选择深度清理。",
    "section.safe": "可安全清理",
    "section.review": "需要确认",
    "section.runScanFirst": "请先运行扫描。",
    "section.noReview": "暂无需要确认的项目。",
    "intelligence.title": "智能判断",
    "intelligence.findings": "算法发现",
    "intelligence.score": "健康评分",
    "intelligence.safeEstimate": "自动安全可回收",
    "intelligence.deepEstimate": "深度可回收",
    "intelligence.pressure": "存储压力",
    "intelligence.scanDuration": "扫描耗时",
    "intelligence.slowestComponent": "最慢组件",
    "intelligence.noFindings": "扫描后会显示智能建议。",
    "component.storage": "存储汇总",
    "component.docker": "Docker",
    "component.backups": "备份",
    "component.resolution": "HAOS 健康",
    "component.homeassistant": "HA 配置",
    "component.journal": "系统日志",
    "component.path_profiles": "目录画像",
    "strategy.title": "清理策略",
    "strategy.description": "基于本机 HAOS 清理经验、官方文档和社区常见方案整理出的安全边界。",
    "strategy.localTitle": "本机清理复盘",
    "strategy.local1": "主要异常集中在 Docker 存储：构建缓存、未使用镜像和 overlay2 派生占用。",
    "strategy.local2": "安全清理优先处理 Docker build cache，避免手动删除 overlay2。",
    "strategy.local3": "备份、数据库、add-on 配置和 Docker volumes 均按用户数据处理，不进入自动清理。",
    "strategy.researchTitle": "网络经验归纳",
    "strategy.research1": "Docker prune 能回收大量空间，但 `--volumes` 和 `image prune -a` 只能放入深度清理。",
    "strategy.research2": "Recorder 数据库应通过 Home Assistant recorder purge 维护，不直接删除数据库文件。",
    "strategy.research3": "journal vacuum 可减少旧日志，但会损失排障历史，因此需要用户确认。",
    "strategy.guardrailTitle": "自动清理护栏",
    "strategy.guardrail.never_delete_docker_volumes": "不自动删除 Docker volumes",
    "strategy.guardrail.never_delete_overlay2_manually": "不手动删除 /mnt/data/docker/overlay2",
    "strategy.guardrail.never_delete_backups_without_selection": "不在未选择时删除备份",
    "strategy.guardrail.never_delete_homeassistant_database_file": "不直接删除 Home Assistant 数据库文件",
    "strategy.guardrail.never_run_docker_image_prune_in_safe_mode": "自动清理不执行 Docker image prune",
    "storage.title": "存储分布",
    "storage.description": "以 HAOS 存储类别为核心展示，便于快速判断空间占用来源。",
    "storage.noMapped": "该 add-on 暂未看到可映射的存储目录。",
    "storage.topEntries": "{category} 主要项目",
    "docker.title": "Docker 系统",
    "docker.description": "查看镜像、容器、构建缓存以及 Docker 可回收空间。",
    "docker.table.type": "类型",
    "docker.table.total": "总数",
    "docker.table.active": "活跃",
    "docker.table.size": "大小",
    "docker.table.reclaimable": "可回收",
    "deep.title": "深度清理",
    "deep.description": "只勾选你理解的项目。TabS Cleaner 不会在未确认时执行深度清理。",
    "deep.confirm": "我已检查这些项目，并确认有近期备份。",
    "deep.disabled": "深度清理已在 add-on 选项中关闭。",
    "deep.noSelection": "请至少选择一个深度清理项目",
    "deep.repositoryCheck": "删除仓库 slug 前，请先勾选“过期仓库”项目",
    "deep.repositoryRequired": "请输入至少一个仓库 slug",
    "deep.journalLabel": "日志保留上限",
    "deep.repositoryLabel": "仓库 slug",
    "deep.repositoryPlaceholder": "example-repo, another-repo",
    "deep.detectedBackups": "检测到的备份",
    "deep.detectedRepositories": "检测到的仓库",
    "deep.manualRepositoryLabel": "手动仓库 slug",
    "deep.noDetectedItems": "暂无可显示项目。",
    "recommendation.recommended": "推荐清理",
    "recommendation.not_recommended": "不推荐清理",
    "deep.reason.stoppedContainersRecommended": "检测到可回收的已停止容器数据，可在确认后清理。",
    "deep.reason.stoppedContainersNotRecommended": "未检测到明显可回收的已停止容器数据，暂不建议执行。",
    "deep.reason.unusedImagesRecommended": "未使用镜像占用较大或当前存储压力较高，确认后可清理。",
    "deep.reason.unusedImagesNotRecommended": "未使用镜像占用不高，清理后可能增加后续下载时间，暂不建议。",
    "deep.reason.journalRecommended": "系统 journal 已超过建议阈值，可裁剪旧日志。",
    "deep.reason.journalNotRecommended": "系统 journal 未明显膨胀，保留日志更利于排障。",
    "deep.reason.backupsRecommended": "发现较旧且已有更新替代的备份，可逐项确认。",
    "deep.reason.backupsNotRecommended": "未发现明确过期的备份，建议保留恢复点。",
    "deep.reason.backupItemRecommended": "较旧且已有多个更新备份，可考虑删除。",
    "deep.reason.backupItemProtected": "受保护备份，不建议删除。",
    "deep.reason.backupItemUnknown": "无法确认备份时间，不建议删除。",
    "deep.reason.backupItemLatest": "这是最新备份，不建议删除。",
    "deep.reason.backupItemRecent": "备份仍较新或替代备份不足，不建议删除。",
    "deep.reason.repositoriesRecommended": "发现未关联已安装 add-on 的第三方仓库，可逐项确认。",
    "deep.reason.repositoriesNotRecommended": "未发现明确过期仓库，未知或仍在使用的仓库不建议删除。",
    "deep.reason.repositoryItemRecommended": "未发现该仓库提供已安装 add-on，可考虑删除。",
    "deep.reason.repositoryItemUnknown": "无法确认仓库使用状态，不建议删除。",
    "deep.reason.repositoryItemOfficial": "官方或本地仓库，不建议删除。",
    "deep.reason.repositoryItemInstalled": "该仓库仍提供已安装 add-on，不建议删除。",
    "deep.reason.repositoryItemKeep": "未满足过期仓库条件，不建议删除。",
    "history.title": "历史记录",
    "history.description": "最近的扫描与清理审计记录。",
    "history.noHistory": "暂无历史记录。",
    "history.unavailable": "历史记录不可用。",
    "history.scanSummary": "已扫描存储：已用 {used}，可用 {free}。",
    "history.cleanupSummary": "{mode}已{status}，共执行 {count} 个动作。",
    "history.status.completed": "完成",
    "history.status.failed": "因错误停止",
    "toast.scanComplete": "扫描完成",
    "toast.safeComplete": "安全清理完成",
    "toast.safeError": "安全清理因错误停止",
    "toast.deepComplete": "深度清理完成",
    "toast.deepError": "深度清理因错误停止",
    "toast.deepDisabled": "深度清理已在 add-on 选项中关闭",
    "card.dockerCache": "Docker 缓存",
    "card.dockerImages": "Docker 镜像",
    "card.backups": "备份",
    "card.haosHealth": "HAOS 健康",
    "hint.safeTarget": "安全清理目标",
    "hint.noEstimate": "暂无估算",
    "hint.restorePoints": "可用恢复点",
    "hint.resolutionCenter": "Resolution 中心",
    "risk.low": "低风险",
    "risk.medium": "中风险",
    "risk.high": "高风险",
    "risk.healthy": "健康",
    "risk.warning": "注意",
    "risk.danger": "危险",
    "risk.critical": "严重",
    "risk.unknown": "未知",
    "mode.scan": "扫描",
    "mode.safe_clean": "安全清理",
    "mode.deep_clean": "深度清理",
    "mode.event": "事件",
    "action.docker_builder_cache.label": "Docker 构建缓存",
    "action.docker_builder_cache.description": "移除未使用的 Docker 构建缓存，不会删除卷或 add-on 数据。",
    "action.docker_system_prune.label": "已停止容器和悬空 Docker 数据",
    "action.docker_system_prune.description": "运行 Docker 默认 system prune，不包含 volumes。该操作需要在 HAOS 上人工确认。",
    "action.resolution_healthcheck.label": "刷新 HAOS 健康检查",
    "action.resolution_healthcheck.description": "请求 Supervisor Resolution 中心刷新健康状态。",
    "action.unused_images.label": "未使用的 Docker 镜像",
    "action.unused_images.description": "删除未被任何容器使用的镜像。后续可能需要重新下载。",
    "action.journal_vacuum.label": "系统日志裁剪",
    "action.journal_vacuum.description": "将系统 journal 限制在指定大小，优先删除较旧日志。",
    "action.delete_backups.label": "所选备份",
    "action.delete_backups.description": "只删除下方明确勾选的备份。",
    "action.delete_repositories.label": "所选过期仓库",
    "action.delete_repositories.description": "按 slug 删除所选 add-on 仓库。不要删除仍提供已安装 add-on 的仓库。",
    "action.estimated": "预计可回收：{value}",
    "action.requiresDeep": "需要在“深度清理”中手动选择。",
    "finding.safe_docker_build_cache": "Docker 构建缓存可安全清理",
    "finding.deep_stopped_containers": "已停止容器需要确认后清理",
    "finding.deep_unused_images": "未使用镜像可深度清理",
    "finding.deep_backups": "备份占用需要逐项选择",
    "finding.deep_journal": "系统日志可按上限裁剪",
    "finding.preserve_docker_volumes": "Docker volumes 已保护",
    "finding.review_recorder_database": "Recorder 数据库建议用 HA 维护",
    "category.backups": "备份",
    "category.homeassistant": "Home Assistant 配置",
    "category.share": "共享目录",
    "category.media": "媒体",
    "category.ssl": "SSL",
    "category.addon_configs": "Add-on 配置",
    "category.addons": "本地 Add-on",
    "category.own_config": "TabS Cleaner 配置",
    "category.unknown": "未知",
  },
  "en": {
    "app.title": "TabS Cleaner",
    "language.label": "Language",
    "nav.smart": "Smart Clean",
    "nav.strategy": "Strategy",
    "nav.storage": "Storage Map",
    "nav.docker": "Docker System",
    "nav.deep": "Deep Clean",
    "nav.history": "History",
    "hero.eyebrow": "Home Assistant OS storage care",
    "hero.title": "Smart storage cleanup for HAOS.",
    "button.scan": "Scan",
    "button.scanning": "Scanning...",
    "button.safeClean": "Clean Safely",
    "button.cleaning": "Cleaning...",
    "button.deepClean": "Run Selected Deep Clean",
    "button.running": "Running...",
    "status.notScanned": "Not scanned",
    "status.unknown": "Unknown",
    "status.clean": "Clean",
    "status.issueCount": "{count} issue(s)",
    "metric.used": "Used",
    "metric.free": "Free",
    "metric.total": "Total",
    "smart.readyTitle": "Ready to scan",
    "smart.readyDescription": "TabS Cleaner checks Docker cache, add-on data, backups, logs, and HAOS health before any cleanup runs.",
    "smart.immediateTitle": "Immediate cleanup recommended",
    "smart.scanCompleteTitle": "Storage scan complete",
    "smart.scanDescription": "Largest category: {category}. Review safe cleanup first, then choose deep cleanup only when needed.",
    "section.safe": "Safe to Clean",
    "section.review": "Review Needed",
    "section.runScanFirst": "Run a scan first.",
    "section.noReview": "No review items yet.",
    "intelligence.title": "Smart Analysis",
    "intelligence.findings": "Algorithm Findings",
    "intelligence.score": "Health score",
    "intelligence.safeEstimate": "Safe reclaimable",
    "intelligence.deepEstimate": "Deep reclaimable",
    "intelligence.pressure": "Storage pressure",
    "intelligence.scanDuration": "Scan duration",
    "intelligence.slowestComponent": "Slowest component",
    "intelligence.noFindings": "Smart recommendations appear after a scan.",
    "component.storage": "Storage summary",
    "component.docker": "Docker",
    "component.backups": "Backups",
    "component.resolution": "HAOS health",
    "component.homeassistant": "HA config",
    "component.journal": "System journal",
    "component.path_profiles": "Path profiles",
    "strategy.title": "Cleanup Strategy",
    "strategy.description": "Safety boundaries distilled from this HAOS cleanup, official docs, and common community workflows.",
    "strategy.localTitle": "Local Cleanup Review",
    "strategy.local1": "The main abnormal growth was Docker storage: build cache, unused images, and overlay2-derived usage.",
    "strategy.local2": "Safe cleanup prioritizes Docker build cache and avoids manual overlay2 deletion.",
    "strategy.local3": "Backups, database files, add-on configs, and Docker volumes are treated as user data and excluded from automatic cleanup.",
    "strategy.researchTitle": "Research Summary",
    "strategy.research1": "Docker prune can reclaim a lot of space, but `--volumes` and `image prune -a` belong in deep cleanup only.",
    "strategy.research2": "Recorder databases should be maintained through Home Assistant recorder purge, not raw file deletion.",
    "strategy.research3": "journal vacuum can reduce old logs, but it removes troubleshooting history and needs confirmation.",
    "strategy.guardrailTitle": "Automatic Cleanup Guardrails",
    "strategy.guardrail.never_delete_docker_volumes": "Never auto-delete Docker volumes",
    "strategy.guardrail.never_delete_overlay2_manually": "Never manually delete /mnt/data/docker/overlay2",
    "strategy.guardrail.never_delete_backups_without_selection": "Never delete backups without selection",
    "strategy.guardrail.never_delete_homeassistant_database_file": "Never delete Home Assistant database files directly",
    "strategy.guardrail.never_run_docker_image_prune_in_safe_mode": "Never run Docker image prune in safe mode",
    "storage.title": "Storage Map",
    "storage.description": "High-level HAOS storage categories, optimized for quick decisions.",
    "storage.noMapped": "No mapped storage directories are visible to this add-on yet.",
    "storage.topEntries": "{category} top entries",
    "docker.title": "Docker System",
    "docker.description": "Images, containers, build cache, and reclaimable Docker storage.",
    "docker.table.type": "Type",
    "docker.table.total": "Total",
    "docker.table.active": "Active",
    "docker.table.size": "Size",
    "docker.table.reclaimable": "Reclaimable",
    "deep.title": "Deep Clean",
    "deep.description": "Select only the items you understand. TabS Cleaner never runs deep cleanup without confirmation.",
    "deep.confirm": "I have reviewed these items and have a recent backup.",
    "deep.disabled": "Deep cleanup is disabled in add-on options.",
    "deep.noSelection": "Select at least one deep clean item",
    "deep.repositoryCheck": "Check Selected stale repositories before deleting repository slugs",
    "deep.repositoryRequired": "Enter at least one repository slug",
    "deep.journalLabel": "Keep journal under",
    "deep.repositoryLabel": "Repository slugs",
    "deep.repositoryPlaceholder": "example-repo, another-repo",
    "deep.detectedBackups": "Detected backups",
    "deep.detectedRepositories": "Detected repositories",
    "deep.manualRepositoryLabel": "Manual repository slugs",
    "deep.noDetectedItems": "No detected items yet.",
    "recommendation.recommended": "Recommended",
    "recommendation.not_recommended": "Not recommended",
    "deep.reason.stoppedContainersRecommended": "Stopped container data is reclaimable after confirmation.",
    "deep.reason.stoppedContainersNotRecommended": "No meaningful stopped-container reclaim was detected.",
    "deep.reason.unusedImagesRecommended": "Unused image reclaim is large or storage pressure is high.",
    "deep.reason.unusedImagesNotRecommended": "Unused image reclaim is low; deleting may only add future download time.",
    "deep.reason.journalRecommended": "System journal exceeds the suggested threshold; older logs can be vacuumed.",
    "deep.reason.journalNotRecommended": "System journal is not inflated; keeping logs helps troubleshooting.",
    "deep.reason.backupsRecommended": "Older backups with newer alternatives were found. Review item by item.",
    "deep.reason.backupsNotRecommended": "No clearly stale backups were found. Keep restore points.",
    "deep.reason.backupItemRecommended": "Older backup with multiple newer backups available.",
    "deep.reason.backupItemProtected": "Protected backup. Not recommended.",
    "deep.reason.backupItemUnknown": "Backup age cannot be verified. Not recommended.",
    "deep.reason.backupItemLatest": "Latest backup. Not recommended.",
    "deep.reason.backupItemRecent": "Backup is still recent or has too few replacements. Not recommended.",
    "deep.reason.repositoriesRecommended": "Third-party repositories with no installed add-ons were found. Review item by item.",
    "deep.reason.repositoriesNotRecommended": "No clearly stale repositories were found. Unknown or active repositories should stay.",
    "deep.reason.repositoryItemRecommended": "No installed add-on was detected from this repository.",
    "deep.reason.repositoryItemUnknown": "Repository usage cannot be verified. Not recommended.",
    "deep.reason.repositoryItemOfficial": "Official or local repository. Not recommended.",
    "deep.reason.repositoryItemInstalled": "This repository still provides an installed add-on.",
    "deep.reason.repositoryItemKeep": "Does not meet stale repository rules. Not recommended.",
    "history.title": "History",
    "history.description": "Recent scans and cleanup reports.",
    "history.noHistory": "No history yet.",
    "history.unavailable": "History is unavailable.",
    "history.scanSummary": "Scanned storage: {used} used, {free} free.",
    "history.cleanupSummary": "{mode} {status} with {count} action(s).",
    "history.status.completed": "completed",
    "history.status.failed": "stopped with errors",
    "toast.scanComplete": "Scan complete",
    "toast.safeComplete": "Safe cleanup complete",
    "toast.safeError": "Safe cleanup stopped with errors",
    "toast.deepComplete": "Deep cleanup complete",
    "toast.deepError": "Deep cleanup stopped with errors",
    "toast.deepDisabled": "Deep cleanup is disabled in add-on options",
    "card.dockerCache": "Docker cache",
    "card.dockerImages": "Docker images",
    "card.backups": "Backups",
    "card.haosHealth": "HAOS health",
    "hint.safeTarget": "Safe cleanup target",
    "hint.noEstimate": "No estimate",
    "hint.restorePoints": "Available restore points",
    "hint.resolutionCenter": "Resolution center",
    "risk.low": "Low",
    "risk.medium": "Medium",
    "risk.high": "High",
    "risk.healthy": "Healthy",
    "risk.warning": "Warning",
    "risk.danger": "Danger",
    "risk.critical": "Critical",
    "risk.unknown": "Unknown",
    "mode.scan": "Scan",
    "mode.safe_clean": "Safe clean",
    "mode.deep_clean": "Deep clean",
    "mode.event": "Event",
    "action.docker_builder_cache.label": "Docker build cache",
    "action.docker_builder_cache.description": "Remove unused Docker builder cache. Does not delete volumes or add-on data.",
    "action.docker_system_prune.label": "Stopped containers and dangling Docker data",
    "action.docker_system_prune.description": "Run Docker system prune without volumes. This action requires manual review on HAOS.",
    "action.resolution_healthcheck.label": "Refresh HAOS health checks",
    "action.resolution_healthcheck.description": "Ask the Supervisor Resolution center to refresh health state.",
    "action.unused_images.label": "Unused Docker images",
    "action.unused_images.description": "Deletes images not used by any container. Re-download may be needed later.",
    "action.journal_vacuum.label": "System journal vacuum",
    "action.journal_vacuum.description": "Caps system journal size. Older logs are removed first.",
    "action.delete_backups.label": "Selected backups",
    "action.delete_backups.description": "Deletes only backups selected below.",
    "action.delete_repositories.label": "Selected stale repositories",
    "action.delete_repositories.description": "Deletes selected add-on repositories by slug. Do not remove repositories that provide installed add-ons.",
    "action.estimated": "Estimated: {value}",
    "action.requiresDeep": "Requires manual selection in Deep Clean.",
    "finding.safe_docker_build_cache": "Docker build cache can be cleaned safely",
    "finding.deep_stopped_containers": "Stopped containers need confirmation",
    "finding.deep_unused_images": "Unused images are deep-clean candidates",
    "finding.deep_backups": "Backups require item selection",
    "finding.deep_journal": "System journal can be vacuumed",
    "finding.preserve_docker_volumes": "Docker volumes are protected",
    "finding.review_recorder_database": "Use HA maintenance for recorder database",
    "category.backups": "Backups",
    "category.homeassistant": "Home Assistant config",
    "category.share": "Share",
    "category.media": "Media",
    "category.ssl": "SSL",
    "category.addon_configs": "Add-on configs",
    "category.addons": "Local add-ons",
    "category.own_config": "TabS Cleaner config",
    "category.unknown": "Unknown",
  },
};

let currentLocale = DEFAULT_LOCALE;
let lastScan = null;
let config = {
  deep_clean_enabled: true,
  journal_vacuum_size: "300M",
  deep_actions: [],
};
const DEFAULT_GUARDRAILS = [
  "never_delete_docker_volumes",
  "never_delete_overlay2_manually",
  "never_delete_backups_without_selection",
  "never_delete_homeassistant_database_file",
  "never_run_docker_image_prune_in_safe_mode",
];

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));

document.addEventListener("DOMContentLoaded", () => {
  currentLocale = normalizeLocale(localStorage.getItem(LOCALE_STORAGE_KEY));
  translatePage();
  $$(".nav-item").forEach((button) => {
    button.addEventListener("click", () => switchView(button.dataset.view));
  });
  $("#languageSelect").addEventListener("change", (event) => {
    setLocale(event.target.value);
  });
  $("#scanButton").addEventListener("click", scan);
  $("#safeCleanButton").addEventListener("click", safeClean);
  $("#deepCleanButton").addEventListener("click", deepClean);
  renderGuardrails(DEFAULT_GUARDRAILS);
  loadConfig();
  loadHistory();
});

function switchView(view) {
  $$(".nav-item").forEach((item) => item.classList.toggle("active", item.dataset.view === view));
  $$(".panel").forEach((panel) => panel.classList.toggle("active", panel.id === `view-${view}`));
}

function setLocale(nextLocale) {
  currentLocale = normalizeLocale(nextLocale);
  localStorage.setItem(LOCALE_STORAGE_KEY, currentLocale);
  translatePage();
  if (lastScan) {
    renderScan(lastScan);
  } else {
    renderDeepActions(config.deep_actions || [], false);
  }
  loadHistory();
}

function normalizeLocale(value) {
  return Object.prototype.hasOwnProperty.call(CATALOGS, value) ? value : DEFAULT_LOCALE;
}

function translatePage() {
  document.documentElement.lang = currentLocale;
  document.title = t("app.title");
  $$("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n, node.textContent);
  });
  const languageSelect = $("#languageSelect");
  if (languageSelect) {
    languageSelect.value = currentLocale;
  }
}

function t(key, fallback = key) {
  return CATALOGS[currentLocale]?.[key] ?? CATALOGS[DEFAULT_LOCALE]?.[key] ?? fallback;
}

function interpolate(key, values) {
  return Object.entries(values).reduce((message, [name, value]) => {
    return message.replaceAll(`{${name}}`, value);
  }, t(key));
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "content-type": "application/json" },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok || payload.ok === false) {
    throw new Error(payload.error || `Request failed: ${response.status}`);
  }
  return payload;
}

async function loadConfig() {
  try {
    config = { ...config, ...(await api("api/config")) };
    renderDeepActions(config.deep_actions || [], false);
  } catch (error) {
    toast(error.message);
  }
}

async function scan() {
  setBusy("#scanButton", t("button.scanning"));
  try {
    lastScan = await api("api/scan", { method: "POST", body: "{}" });
    config = { ...config, ...pickConfig(lastScan) };
    renderScan(lastScan);
    toast(t("toast.scanComplete"));
  } catch (error) {
    toast(error.message);
  } finally {
    setReady("#scanButton", t("button.scan"));
  }
}

async function safeClean() {
  setBusy("#safeCleanButton", t("button.cleaning"));
  try {
    const report = await api("api/clean/safe", { method: "POST", body: "{}" });
    toast(report.ok ? t("toast.safeComplete") : t("toast.safeError"));
    await scan();
    await loadHistory();
  } catch (error) {
    toast(error.message);
  } finally {
    setReady("#safeCleanButton", t("button.safeClean"));
  }
}

async function deepClean() {
  const actions = $$(".deep-action:checked").map((input) => input.value);
  const confirmed = $("#deepConfirm").checked;
  const backupSlugs = $$(".backup-action:checked").map((input) => input.value);
  const repositorySlugs = unique([
    ...$$(".repository-action:checked").map((input) => input.value),
    ...parseSlugList($("#repositorySlugs")?.value || ""),
  ]);
  const journalSize = $("#journalSizeInput")?.value || config.journal_vacuum_size || "300M";
  if (!config.deep_clean_enabled) {
    toast(t("toast.deepDisabled"));
    return;
  }
  if (backupSlugs.length && !actions.includes("delete_backups")) {
    actions.push("delete_backups");
  }
  if (repositorySlugs.length && !actions.includes("delete_repositories")) {
    toast(t("deep.repositoryCheck"));
    return;
  }
  if (actions.includes("delete_repositories") && !repositorySlugs.length) {
    toast(t("deep.repositoryRequired"));
    return;
  }
  if (!actions.length && !backupSlugs.length && !repositorySlugs.length) {
    toast(t("deep.noSelection"));
    return;
  }
  setBusy("#deepCleanButton", t("button.running"));
  try {
    const report = await api("api/clean/deep", {
      method: "POST",
      body: JSON.stringify({
        actions,
        confirmed,
        backup_slugs: backupSlugs,
        repository_slugs: repositorySlugs,
        journal_vacuum_size: journalSize,
      }),
    });
    toast(report.ok ? t("toast.deepComplete") : t("toast.deepError"));
    await scan();
    await loadHistory();
  } catch (error) {
    toast(error.message);
  } finally {
    setReady("#deepCleanButton", t("button.deepClean"));
  }
}

function renderScan(data) {
  const storage = data.storage || {};
  $("#storageRing").style.setProperty("--used", storage.used_percent || 0);
  $("#usedPercent").textContent = `${storage.used_percent || 0}%`;
  $("#riskLabel").textContent = t(`risk.${storage.risk || "unknown"}`, title(storage.risk || "unknown"));
  $("#usedText").textContent = storage.human?.used || "--";
  $("#freeText").textContent = storage.human?.free || "--";
  $("#totalText").textContent = storage.human?.total || "--";
  $("#smartTitle").textContent = storage.risk === "critical" ? t("smart.immediateTitle") : t("smart.scanCompleteTitle");
  $("#smartDescription").textContent = interpolate("smart.scanDescription", {
    category: label(storage.largest_category?.name || "unknown"),
  });
  $("#safeCleanButton").disabled = false;
  renderCards(data);
  renderSafeActions(data.safe_actions || []);
  renderDeepActions(data.deep_actions || []);
  renderStorageBars(storage);
  renderPathProfiles(data.path_profiles || {});
  renderDocker(data.docker || {});
  renderIntelligence(data);
}

function renderCards(data) {
  const dockerRows = data.docker?.system_df || [];
  const buildCache = dockerRows.find((row) => row.type === "Build Cache");
  const imageRow = dockerRows.find((row) => row.type === "Images");
  const backupCount = data.backups?.backups?.length || 0;
  const issueCount = data.resolution?.issues?.length || 0;
  $("#summaryCards").innerHTML = [
    card(t("card.dockerCache"), buildCache?.reclaimable || t("status.unknown"), t("hint.safeTarget")),
    card(t("card.dockerImages"), imageRow?.size || t("status.unknown"), imageRow?.reclaimable || t("hint.noEstimate")),
    card(t("card.backups"), `${backupCount}`, t("hint.restorePoints")),
    card(t("card.haosHealth"), issueCount ? interpolate("status.issueCount", { count: issueCount }) : t("status.clean"), t("hint.resolutionCenter")),
  ].join("");
}

function renderSafeActions(actions) {
  $("#safeActions").innerHTML = actions.map((action) => actionCard(action)).join("") || empty(t("section.runScanFirst"));
}

function renderDeepActions(actions, updateReview = true) {
  if (updateReview) {
    $("#reviewActions").innerHTML = actions.map((action) => actionCard(action, true)).join("") || empty(t("section.noReview"));
  } else {
    $("#reviewActions").innerHTML = empty(t("section.runScanFirst"));
  }
  if (!config.deep_clean_enabled) {
    $("#deepActions").innerHTML = empty(t("deep.disabled"));
    $("#deepCleanButton").disabled = true;
    return;
  }
  $("#deepActions").innerHTML = actions.map((action) => deepCard(action)).join("");
  $("#deepCleanButton").disabled = false;
}

function renderIntelligence(data) {
  const intelligence = data.intelligence || {};
  const timings = data.timings || {};
  const slowest = slowestTiming(timings);
  const score = intelligence.score ?? "--";
  $("#intelligenceSummary").innerHTML = [
    smartMetric(t("intelligence.score"), `${score}`),
    smartMetric(t("intelligence.safeEstimate"), intelligence.safe_reclaimable || "--"),
    smartMetric(t("intelligence.deepEstimate"), intelligence.deep_reclaimable || "--"),
    smartMetric(t("intelligence.pressure"), t(`risk.${intelligence.pressure || "unknown"}`)),
    smartMetric(t("intelligence.scanDuration"), `${timings.total ?? data.duration_ms ?? "--"} ms`),
    smartMetric(t("intelligence.slowestComponent"), slowest ? `${t(`component.${slowest.name}`, slowest.name)} · ${slowest.duration} ms` : "--"),
  ].join("");

  const findings = intelligence.findings || [];
  $("#intelligenceFindings").innerHTML = findings.map((finding) => findingCard(finding)).join("") || empty(t("intelligence.noFindings"));
  renderGuardrails(intelligence.guardrails || DEFAULT_GUARDRAILS);
}

function slowestTiming(timings) {
  return Object.entries(timings || {})
    .filter(([name]) => name !== "total")
    .map(([name, duration]) => ({ name, duration: Number(duration || 0) }))
    .sort((a, b) => b.duration - a.duration)[0];
}

function smartMetric(labelText, value) {
  return `<div class="smart-metric"><span>${escapeHtml(labelText)}</span><strong>${escapeHtml(value)}</strong></div>`;
}

function findingCard(finding) {
  return `<div class="action finding">
    <span class="risk ${escapeHtml(finding.risk || "medium")}">${escapeHtml(t(`risk.${finding.risk || "medium"}`))}</span>
    <h4>${escapeHtml(t(`finding.${finding.id}`, finding.id))}</h4>
    <p>${escapeHtml(finding.detail || "")}</p>
    <small>${escapeHtml(interpolate("action.estimated", { value: finding.estimate || "--" }))}</small>
  </div>`;
}

function renderGuardrails(guardrails) {
  const node = $("#guardrailList");
  if (!node) return;
  node.innerHTML = (guardrails || DEFAULT_GUARDRAILS).map((item) => `
    <div class="guardrail-item">${escapeHtml(t(`strategy.guardrail.${item}`, item))}</div>
  `).join("");
}

function renderStorageBars(storage) {
  const categories = storage.categories || {};
  const entries = Object.entries(categories).sort((a, b) => b[1] - a[1]);
  const max = entries[0]?.[1] || 1;
  $("#storageBars").innerHTML = entries.map(([name, bytes]) => {
    const width = Math.max(2, Math.round((bytes / max) * 100));
    return `<div class="bar-row">
      <div class="bar-meta"><strong>${escapeHtml(label(name))}</strong><span>${escapeHtml(formatBytes(bytes))}</span></div>
      <div class="bar-track"><div class="bar-fill" style="--width:${width}%"></div></div>
    </div>`;
  }).join("") || empty(t("storage.noMapped"));
}

function renderPathProfiles(profiles) {
  const entries = Object.entries(profiles || {});
  $("#pathProfiles").innerHTML = entries.map(([name, profile]) => {
    const topEntries = profile.top_entries || [];
    if (!topEntries.length) return "";
    return `<div class="path-profile">
      <h3>${escapeHtml(interpolate("storage.topEntries", { category: label(name) }))}</h3>
      ${topEntries.map((entry) => `
        <div class="path-entry">
          <span>${escapeHtml(entry.name || entry.path)}</span>
          <strong>${escapeHtml(entry.size || formatBytes(entry.size_bytes))}</strong>
        </div>
      `).join("")}
    </div>`;
  }).join("");
}

function renderDocker(docker) {
  const rows = docker.system_df || [];
  $("#dockerTable").innerHTML = `<table>
    <thead><tr><th>${escapeHtml(t("docker.table.type"))}</th><th>${escapeHtml(t("docker.table.total"))}</th><th>${escapeHtml(t("docker.table.active"))}</th><th>${escapeHtml(t("docker.table.size"))}</th><th>${escapeHtml(t("docker.table.reclaimable"))}</th></tr></thead>
    <tbody>${rows.map((row) => `<tr><td>${escapeHtml(row.type)}</td><td>${escapeHtml(row.total)}</td><td>${escapeHtml(row.active)}</td><td>${escapeHtml(row.size)}</td><td>${escapeHtml(row.reclaimable)}</td></tr>`).join("")}</tbody>
  </table>`;
}

async function loadHistory() {
  try {
    const data = await api("api/history");
    $("#historyList").innerHTML = (data.history || []).map((entry) => `
      <div class="history-item">
        <strong>${escapeHtml(t(`mode.${entry.mode || "event"}`, title(entry.mode || "event")))}</strong>
        <p>${escapeHtml(historySummary(entry))}</p>
        <small>${escapeHtml(entry.timestamp || "")}</small>
      </div>
    `).join("") || empty(t("history.noHistory"));
  } catch {
    $("#historyList").innerHTML = empty(t("history.unavailable"));
  }
}

function card(labelText, value, hint) {
  return `<div class="metric-card"><div class="metric-label">${escapeHtml(labelText)}</div><div class="metric-value">${escapeHtml(value)}</div><small>${escapeHtml(hint)}</small></div>`;
}

function actionLabel(action) {
  return t(`action.${action.id}.label`, action.label || action.id);
}

function actionDescription(action) {
  return t(`action.${action.id}.description`, action.description || "");
}

function actionCard(action, review = false) {
  return `<div class="action">
    <div class="badge-row">
      <span class="risk ${escapeHtml(action.risk || "low")}">${escapeHtml(t(`risk.${action.risk || "low"}`, title(action.risk || "low")))}</span>
      ${decisionBadge(action)}
    </div>
    <h4>${escapeHtml(actionLabel(action))}</h4>
    <p>${escapeHtml(actionDescription(action))}</p>
    ${action.reason_key ? `<small>${escapeHtml(reasonText(action))}</small>` : ""}
    ${action.estimate ? `<small>${escapeHtml(interpolate("action.estimated", { value: action.estimate }))}</small>` : ""}
    ${review ? `<small>${escapeHtml(t("action.requiresDeep"))}</small>` : ""}
  </div>`;
}

function deepCard(action) {
  const backupItems = action.id === "delete_backups" ? itemChecklist(action.items || [], "backup-action") : "";
  const repositoryItems = action.id === "delete_repositories" ? itemChecklist(action.items || [], "repository-action") : "";
  const journalControl = action.id === "journal_vacuum"
    ? `<label class="field-line">${escapeHtml(t("deep.journalLabel"))}<input id="journalSizeInput" value="${escapeHtml(action.journal_vacuum_size || config.journal_vacuum_size || "300M")}" /></label>`
    : "";
  const repositoryControl = action.id === "delete_repositories"
    ? `<label class="field-line">${escapeHtml(t("deep.manualRepositoryLabel"))}<input id="repositorySlugs" placeholder="${escapeHtml(t("deep.repositoryPlaceholder"))}" /></label>`
    : "";
  const checkbox = action.id === "delete_backups"
    ? ""
    : `<input class="deep-action" type="checkbox" value="${escapeHtml(action.id)}" />`;
  return `<div class="deep-card">
    ${checkbox}
    <div>
      <div class="badge-row">
        <span class="risk ${escapeHtml(action.risk || "medium")}">${escapeHtml(t(`risk.${action.risk || "medium"}`, title(action.risk || "medium")))}</span>
        ${decisionBadge(action)}
      </div>
      <h3>${escapeHtml(actionLabel(action))}</h3>
      <p>${escapeHtml(actionDescription(action))}</p>
      ${action.reason_key ? `<small class="decision-reason">${escapeHtml(reasonText(action))}</small>` : ""}
      ${action.estimate ? `<small>${escapeHtml(interpolate("action.estimated", { value: action.estimate }))}</small>` : ""}
      ${journalControl}
      ${repositoryControl}
      ${repositoryItems}
      ${backupItems}
    </div>
  </div>`;
}

function itemChecklist(items, className) {
  if (!items.length) {
    return `<div class="cleanup-items">${empty(t("deep.noDetectedItems"))}</div>`;
  }
  return `<div class="cleanup-items">${items.map((item) => `
    <label class="cleanup-item ${escapeHtml(item.recommendation || "not_recommended")}">
      <input class="${escapeHtml(className)}" type="checkbox" value="${escapeHtml(item.slug)}" />
      <span>
        <strong>${escapeHtml(item.name || item.slug)}</strong>
        <small>${escapeHtml(itemDetail(item))}</small>
        <small>${escapeHtml(reasonText(item))}</small>
      </span>
      ${decisionBadge(item)}
    </label>
  `).join("")}</div>`;
}

function decisionBadge(item) {
  if (!item.recommendation) return "";
  const key = `recommendation.${item.recommendation}`;
  return `<span class="decision ${escapeHtml(item.recommendation)}">${escapeHtml(t(key, title(item.recommendation)))}</span>`;
}

function reasonText(item) {
  return item.reason || t(item.reason_key || "", item.reason_key || "");
}

function itemDetail(item) {
  const bits = [];
  const size = item.size || (item.size_bytes ? formatBytes(item.size_bytes) : "");
  if (size) bits.push(size);
  if (item.age_days !== null && item.age_days !== undefined) bits.push(`${item.age_days}d`);
  if (item.source) bits.push(item.source);
  return bits.join(" · ");
}

function empty(message) {
  return `<div class="action"><p>${message}</p></div>`;
}

function historySummary(entry) {
  const result = entry.result || {};
  if (entry.mode === "scan" && result.storage?.human) {
    return interpolate("history.scanSummary", {
      used: result.storage.human.used || t("status.unknown"),
      free: result.storage.human.free || t("status.unknown"),
    });
  }
  if (entry.mode === "safe_clean" || entry.mode === "deep_clean") {
    return interpolate("history.cleanupSummary", {
      mode: t(`mode.${entry.mode}`, entry.mode),
      status: result.ok === false ? t("history.status.failed") : t("history.status.completed"),
      count: result.results?.length || 0,
    });
  }
  return entry.summary || "";
}

function setBusy(selector, label) {
  const button = $(selector);
  button.disabled = true;
  button.textContent = label;
}

function setReady(selector, label) {
  const button = $(selector);
  button.disabled = false;
  button.textContent = label;
}

function toast(message) {
  const node = $("#toast");
  node.textContent = message;
  node.classList.add("show");
  setTimeout(() => node.classList.remove("show"), 2600);
}

function pickConfig(data) {
  return {
    deep_clean_enabled: data.deep_clean_enabled,
    journal_vacuum_size: data.journal_vacuum_size,
    deep_actions: data.deep_actions || [],
  };
}

function parseSlugList(value) {
  return String(value)
    .split(/[\s,]+/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function unique(items) {
  return Array.from(new Set(items.filter(Boolean)));
}

function title(value) {
  return String(value).replace(/_/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function label(value) {
  return t(`category.${value}`, title(value).replace("Homeassistant", "Home Assistant"));
}

function formatBytes(bytes) {
  const units = ["B", "KB", "MB", "GB", "TB"];
  let size = Number(bytes || 0);
  for (const unit of units) {
    if (Math.abs(size) < 1024 || unit === units[units.length - 1]) {
      return unit === "B" ? `${Math.round(size)} B` : `${size.toFixed(1)} ${unit}`;
    }
    size /= 1024;
  }
  return `${size.toFixed(1)} TB`;
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  }[char]));
}
