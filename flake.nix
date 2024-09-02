{
  description = "ilzabot";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    devshell.url = "github:numtide/devshell";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, devshell, flake-utils }:
    flake-utils.lib.eachDefaultSystem(system:
      let
        inherit (nixpkgs) lib;
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
          config.allowBroken = true;
          overlays = [
            devshell.overlays.default
            # self.overlay
          ];
        };
      in
        {
          packages = {
          };

          devShell = import ./devshell.nix { inherit pkgs; };
        }
    );
}
