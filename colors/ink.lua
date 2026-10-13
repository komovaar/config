-- Ink UI with restrained syntax accents for readable code.
vim.opt.termguicolors = true
vim.opt.background = "dark"
vim.cmd "highlight clear"
vim.g.colors_name = "ink"

local p = { bg = "#141414", panel = "#202020", selection = "#393939", fg = "#eeeeee", dim = "#999999", muted = "#707070", white = "#ffffff" }
local function hl(name, spec)
  vim.api.nvim_set_hl(0, name, spec)
end

-- Convert built-in/plugin defaults to grayscale, including unlisted groups.
for name, spec in pairs(vim.api.nvim_get_hl(0, {})) do
  if not spec.link then
    for _, key in ipairs { "fg", "bg", "sp" } do
      if spec[key] then
        local value = spec[key]
        local r, g, b = math.floor(value / 65536), math.floor(value / 256) % 256, value % 256
        local gray = math.floor(0.2126 * r + 0.7152 * g + 0.0722 * b + 0.5)
        spec[key] = gray * 65793
      end
    end
    spec.ctermfg, spec.ctermbg = nil, nil
    hl(name, spec)
  end
end

hl("Normal", { fg = p.fg, bg = p.bg })
hl("NormalNC", { link = "Normal" })
hl("NormalFloat", { fg = p.fg, bg = p.panel })
hl("FloatBorder", { fg = p.muted, bg = p.panel })
for _, name in ipairs { "SignColumn", "FoldColumn", "EndOfBuffer" } do
  hl(name, { fg = p.muted, bg = p.bg })
end
hl("LineNr", { fg = p.muted })
hl("CursorLineNr", { fg = p.white, bold = true })
hl("CursorLine", { bg = p.panel })
hl("Cursor", { fg = p.bg, bg = p.white })
hl("Visual", { bg = p.selection })
hl("Search", { fg = p.bg, bg = p.dim })
hl("IncSearch", { fg = p.bg, bg = p.white, bold = true })
hl("CurSearch", { link = "IncSearch" })
hl("MatchParen", { fg = p.white, bg = p.selection, bold = true })
hl("WinSeparator", { fg = p.selection })
hl("StatusLine", { fg = p.white, bg = p.selection, bold = true })
hl("StatusLineNC", { fg = p.dim, bg = p.panel })
hl("TabLine", { fg = p.dim, bg = p.panel })
hl("TabLineFill", { bg = p.panel })
hl("TabLineSel", { fg = p.white, bg = p.selection, bold = true })
hl("Pmenu", { fg = p.fg, bg = p.panel })
hl("PmenuSel", { fg = p.bg, bg = p.white, bold = true })
hl("PmenuSbar", { bg = p.selection })
hl("PmenuThumb", { bg = p.dim })
hl("Comment", { fg = p.muted, italic = true })
for _, name in ipairs { "Keyword", "Statement", "Conditional", "Repeat", "Exception", "PreProc", "Type", "StorageClass", "Structure", "Typedef" } do
  hl(name, { fg = p.white, bold = true })
end
for _, name in ipairs { "String", "Character", "Number", "Boolean", "Float", "Constant" } do
  hl(name, { fg = p.dim })
end
for _, name in ipairs { "Identifier", "Function", "Operator", "Delimiter", "Special" } do
  hl(name, { fg = p.fg })
end
hl("Todo", { fg = p.white, bold = true, underline = true })
hl("Title", { fg = p.white, bold = true })
hl("Directory", { fg = p.fg, bold = true })
hl("Error", { fg = p.white, bg = p.selection, bold = true })
hl("ErrorMsg", { fg = p.white, bold = true })
hl("WarningMsg", { fg = p.dim, bold = true })
hl("NonText", { fg = p.muted })
hl("Whitespace", { fg = p.selection })
hl("Folded", { fg = p.dim, bg = p.panel })
for _, severity in ipairs { "Error", "Warn", "Info", "Hint", "Ok" } do
  local color = severity == "Error" and p.white or p.dim
  hl("Diagnostic" .. severity, { fg = color, bold = severity == "Error" })
  hl("DiagnosticVirtualText" .. severity, { fg = color, bg = p.panel })
  hl("DiagnosticUnderline" .. severity, { sp = color, undercurl = true })
end
hl("DiffAdd", { bg = "#282828" })
hl("DiffChange", { bg = p.panel })
hl("DiffDelete", { fg = p.muted, bg = p.panel })
hl("DiffText", { bg = p.selection, bold = true })
for _, name in ipairs { "Added", "Changed", "Removed" } do
  hl(name, { fg = p.dim })
end
hl("NvimTreeNormal", { fg = p.fg, bg = p.bg })
hl("NvimTreeNormalNC", { link = "NvimTreeNormal" })
hl("NvimTreeRootFolder", { fg = p.white, bold = true })
for _, name in ipairs { "FolderName", "OpenedFolderName", "FolderIcon", "GitDirty", "GitNew", "GitDeleted", "GitStaged", "ExecFile", "SpecialFile", "ImageFile" } do
  hl("NvimTree" .. name, { fg = p.fg })
end

-- Treesitter and semantic tokens inherit the same monochrome syntax styles.
for capture, target in pairs {
  comment = "Comment", keyword = "Keyword", string = "String", character = "Character",
  number = "Number", boolean = "Boolean", constant = "Constant", variable = "Identifier",
  ["function"] = "Function", type = "Type", operator = "Operator", punctuation = "Delimiter",
  property = "Identifier", module = "Identifier", tag = "Keyword",
} do
  hl("@" .. capture, { link = target })
end
for token, target in pairs { class = "Type", struct = "Type", enum = "Type", interface = "Type", type = "Type", parameter = "Identifier", variable = "Identifier", property = "Identifier", ["function"] = "Function", method = "Function", keyword = "Keyword", comment = "Comment", string = "String", number = "Number" } do
  hl("@lsp.type." .. token, { link = target })
end

-- Soft code accents; the surrounding editor remains monochrome.
for _, name in ipairs { "Keyword", "Statement", "Conditional", "Repeat", "Exception", "PreProc", "StorageClass" } do
  hl(name, { fg = "#c4b5d5", bold = true })
end
for _, name in ipairs { "Type", "Structure", "Typedef" } do
  hl(name, { fg = "#cfc3a6" })
end
hl("Function", { fg = "#aac9dd", bold = true })
hl("String", { fg = "#b4c9ae" })
hl("Character", { link = "String" })
for _, name in ipairs { "Number", "Float", "Boolean", "Constant" } do
  hl(name, { fg = "#d5b99e" })
end
hl("Comment", { fg = "#929292", italic = true })
hl("Delimiter", { fg = "#b0b0b0" })
hl("Operator", { fg = "#d5d5d5" })
for capture, target in pairs {
  ["function.call"] = "Function", ["function.builtin"] = "Function",
  ["function.method"] = "Function", ["function.method.call"] = "Function",
  ["constructor"] = "Type", ["type.builtin"] = "Type",
  ["variable.builtin"] = "Constant", ["constant.builtin"] = "Constant",
  ["string.escape"] = "Constant", ["string.regexp"] = "String",
  ["variable.parameter"] = "Identifier", ["variable.member"] = "Identifier",
  ["punctuation.bracket"] = "Delimiter", ["punctuation.delimiter"] = "Delimiter",
  ["markup.heading"] = "Title", ["markup.raw"] = "String",
} do
  hl("@" .. capture, { link = target })
end
