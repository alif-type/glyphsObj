#
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import difflib
import os.path
import re
import sys
from io import StringIO
from textwrap import dedent

import glyphsObj
from glyphsObj.writer import Writer


def write_to_lines(glyphs_object):
    """
    Use the Writer to write the given object to a StringIO.
    Return an array of lines ready for diffing.
    """
    string = StringIO()
    writer = Writer(string)
    writer.write(glyphs_object)
    return string.getvalue().splitlines()


class AssertLinesEqual:
    def assertLinesEqual(self, expected, actual, message):
        if actual != expected:
            if len(actual) < len(expected):
                sys.stderr.write(
                    dedent(
                        """\
                    WARNING: the actual text is shorter that the expected text.
                             Some information may be LOST!
                    """
                    )
                )
            for line in difflib.unified_diff(
                expected, actual, fromfile="<expected>", tofile="<actual>"
            ):
                if not line.endswith("\n"):
                    line += "\n"
                sys.stderr.write(line)
            self.fail(message)


class AssertParseWriteRoundtrip(AssertLinesEqual):
    def assertParseWriteRoundtrip(self, filename):
        with open(filename) as f:
            expected = f.read().splitlines()
            f.seek(0, 0)
            font = glyphsObj.load(f)
        actual = write_to_lines(font)
        # Roundtrip again to check idempotence
        font = glyphsObj.loads("\n".join(actual))
        actual_idempotent = write_to_lines(font)
        with open("expected.txt", "w") as f:
            f.write("\n".join(expected))
        with open("actual.txt", "w") as f:
            f.write("\n".join(actual))
        with open("actual_indempotent.txt", "w") as f:
            f.write("\n".join(actual_idempotent))
        # Assert idempotence first, because if that fails it's a big issue
        self.assertLinesEqual(
            actual,
            actual_idempotent,
            "The parser/writer should be idempotent. BIG PROBLEM!",
        )
        self.assertLinesEqual(
            expected, actual, "The writer should output exactly what the parser read"
        )


APP_VERSION_RE = re.compile('\\.appVersion = "(.*)"')


def glyphs_files(directory):
    for root, _dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".glyphs"):
                yield os.path.join(root, filename)


def app_version(filename):
    with open(filename) as fp:
        for line in fp:
            m = APP_VERSION_RE.match(line)
            if m:
                return m.group(1)
    return "no_version"
