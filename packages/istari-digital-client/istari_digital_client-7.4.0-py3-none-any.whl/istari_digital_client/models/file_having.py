import abc
from typing import List

from istari_digital_client.models.file_revision import FileRevision
from istari_digital_client.models.file_revision_having import FileRevisionHaving


class FileHaving(FileRevisionHaving, abc.ABC):
    @property
    def revisions(self) -> List[FileRevision]:
        file = getattr(self, "file", None)

        if file is None:
            raise ValueError("file is not set")

        return file.revisions

    @property
    def revision(self) -> FileRevision:
        return self.revisions[-1]
