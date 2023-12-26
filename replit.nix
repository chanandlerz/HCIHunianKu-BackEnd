{ pkgs }: {
  deps = [
    pkgs.rustc
    pkgs.pkg-config
    pkgs.openssl
    pkgs.libxcrypt
    pkgs.libiconv
    pkgs.cargo
    pkgs.ls /nix/store/*-python*/bin
    pkgs.ccc
    pkgs.python39Packages.clvm-tools
  ];
}