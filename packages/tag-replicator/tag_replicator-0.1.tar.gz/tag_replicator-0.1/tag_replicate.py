import argparse
import sys
from taggers import get_tagger

def confirm_and_apply(source_tags, target_tags, new_tags, target_id, tagger, clean):
    print("\nCurrent tags on target:")
    print(target_tags)
    print("\nNew tags to be applied:")
    print(new_tags)
    if clean:
        print("\nNote: Tags not present in source will be removed from the target.")
    answer = input("\nDo you want to proceed with the tag update? (yes/no): ")
    if answer.lower() == 'yes':
        tagger.apply_tags(target_id, new_tags, clean)
        print("\nTags updated successfully.")
    else:
        print("\nOperation cancelled.")

def main():
    parser = argparse.ArgumentParser(description='Replicate tags from one AWS resource to another.')
    parser.add_argument('--type', required=True, help='Resource type (ec2, s3, ebs, snapshot, elb, rds, etc.)')
    parser.add_argument('--model', required=True, help='Source resource ID or name')
    parser.add_argument('--target', required=True, help='Target resource ID or name')
    parser.add_argument('--clean', action='store_true', help='If set, tags not in the source will be removed from the target')

    args = parser.parse_args()

    tagger = get_tagger(args.type)
    if not tagger:
        print(f"Unsupported resource type: {args.type}")
        sys.exit(1)

    source_tags = tagger.get_tags(args.model)
    target_tags = tagger.get_tags(args.target)

    if args.clean:
        new_tags = source_tags
    else:
        new_tags = target_tags.copy()
        new_tags.update(source_tags)

    confirm_and_apply(source_tags, target_tags, new_tags, args.target, tagger, args.clean)

if __name__ == '__main__':
    main()