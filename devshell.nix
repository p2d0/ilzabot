{ pkgs }:

with pkgs;

# Configure your development environment.
devshell.mkShell rec {
  name = "Ilzabot";
  motd = ''
Entered Ilzabot app development environment.
'';

  env = [
    # {
    #   name = "ANDROID_HOME";
    #   value = "android-sdk/share/android-sdk";
    # }
    {
      name = "LD_LIBRARY_PATH";
      prefix = lib.makeLibraryPath [
        stdenv.cc.cc
        pkgs.glib
        pkgs.libglvnd
        pkgs.zlib
        pkgs.dlib
      ];
    }
  ];


  # NIX_LD = lib.fileContents "${stdenv.cc}/nix-support/dynamic-linker";
  packages = [
    # stdenv.cc.cc
    # pkgs.glib
    # pkgs.libglvnd
    # pkgs.zlib
    # pkgs.dlib
    pkgs.imagemagick
    pkgs.ffmpeg
    pkgs.dlib
    pkgs.cmake
    (pkgs.python39.withPackages(ps: [ ps.pip ]))
  ];
}
