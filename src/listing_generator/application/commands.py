from listing_generator.application.dto import (
    FormatTemplateAndSaveDTO,
    FormatTemplateDTO,
)
from listing_generator.application.entities import ListingSource
from listing_generator.application.filters import (
    ExcludeExtensionFilter,
    EmptyFilter,
    IncludeExtensionFilter,
    EmptyFileFilter,
    ExcludeFileNameFilter,
    InlcudeFileNameFilter,
)


class FormatTemplateAndSaveCommand:
    def execute(self, dto: FormatTemplateAndSaveDTO):
        file_list = dto.file_list
        filter = ExcludeFileNameFilter(
            InlcudeFileNameFilter(
                ExcludeExtensionFilter(
                    IncludeExtensionFilter(
                        EmptyFilter(file_list),
                        included_extensions=dto.included_extensions,
                    ),
                    excluded_extensions=dto.excluded_extensions,
                ),
                included_filenames=dto.included_filenames,
            ),
            excluded_filenames=dto.excluded_filenames,
        )
        if dto.skip_empty_files:
            filter = EmptyFileFilter(filter)
        items = []
        file_list = filter.filter()
        for path in file_list:
            path_text = path.read_text(encoding="utf-8")
            if dto.minimize_line_count:
                path_text = path_text.replace("\n\n", "\n")
            items.append(
                ListingSource(
                    path=path.relative_to(dto.source_directory),
                    text=path_text,
                )
            )
        formatter = dto.formatter_type(dto.template_path)
        document = formatter.render(items)
        document.save(dto.out_file_path)


class FormatTemplateCommand:
    def execute(self, dto: FormatTemplateDTO):
        file_list = dto.file_list
        filter = ExcludeFileNameFilter(
            InlcudeFileNameFilter(
                ExcludeExtensionFilter(
                    IncludeExtensionFilter(
                        EmptyFilter(file_list),
                        included_extensions=dto.included_extensions,
                    ),
                    excluded_extensions=dto.excluded_extensions,
                ),
                included_filenames=dto.included_filenames,
            ),
            excluded_filenames=dto.excluded_filenames,
        )
        if dto.skip_empty_files:
            filter = EmptyFileFilter(filter)
        items = []
        file_list = filter.filter()
        print(file_list)

        items = []
        for path in file_list:
            path_text = path.read_text(encoding="utf-8")
            if dto.minimize_line_count:
                path_text = path_text.replace("\n\n", "\n")
            items.append(
                ListingSource(
                    path=path.relative_to(dto.source_directory),
                    text=path_text,
                )
            )
        formatter = dto.formatter_type(dto.template_path)
        document = formatter.render(items)
        return document
