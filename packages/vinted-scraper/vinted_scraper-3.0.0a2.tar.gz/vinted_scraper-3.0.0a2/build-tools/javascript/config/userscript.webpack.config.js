/* eslint-disable */
const path = require("path");
const { monkey } = require("webpack-monkey");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = monkey({
  entry: {
    // <add-your-user-scripts-here>
  },
  plugins: [new MiniCssExtractPlugin()],
  module: {
    rules: [
      {
        test: /\.s[ac]ss$/i,
        use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"],
      },
    ],
  },
  output: {
    path: path.resolve(__dirname, "dist"),
  },
  performance: {
    hints: false,
    maxEntrypointSize: 512000,
    maxAssetSize: 512000,
  },
});
