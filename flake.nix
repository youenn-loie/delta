{
  inputs = {
    nixpie.url = "git+https://gitlab.cri.epita.fr/cri/infrastructure/nixpie.git";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs = { self, nixpie, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        inherit (nixpie.inputs) nixpkgs;
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ poetry2nix.overlay ];
        };
        poetryEnv = pkgs.poetry2nix.mkPoetryEnv {
          projectDir = ./.;
        };
      in
        {
          devShell = pkgs.mkShell {
            buildInputs =  [
              poetryEnv

              pkgs.poetry
            ];
          };
        });
}
