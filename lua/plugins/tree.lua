return {
  "nvim-tree/nvim-tree.lua",
  version = "*",
  lazy = false,
  dependencies = {
    "nvim-tree/nvim-web-devicons",
  },
  config = function()
    require("nvim-tree").setup {
      renderer = { icons = { web_devicons = { file = { color = false }, folder = { color = false } } } },
    }

    vim.keymap.set("n", "<leader>e", ":NvimTreeToggle<cr>")
  end,
}
