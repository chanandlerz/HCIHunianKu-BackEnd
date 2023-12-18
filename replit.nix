{ pkgs }: {
  deps = [
    pkgs.rustc
    pkgs.pkg-config
    pkgs.openssl
    pkgs.libxcrypt
    pkgs.libiconv
    pkgs.cargo
    pkgs.imagemagick6_light
    pkgs.1
  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.rustc
      pkgs.libxcrypt
    ];
  };
}