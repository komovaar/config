return {
  "nvim-treesitter/nvim-treesitter",
  branch = "master", -- old API that this config was written for
  lazy = false,
  build = ":TSUpdate",
  config = function()
    require("nvim-treesitter.configs").setup({
      ensure_installed = {
        "python", "html", "css", "matlab",
        "javascript", "lua", "vim", "vimdoc", "query",
      },
      sync_install = false,
      auto_install = true,
      highlight = {
        enable = true,
        additional_vim_regex_highlighting = false,
      },
      indent = { enable = true },
    })
  end,
}
