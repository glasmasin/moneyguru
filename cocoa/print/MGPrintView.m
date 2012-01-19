/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import "MGPrintView.h"
#import "Utils.h"
#import "ObjP.h"
#import "MGConst.h"

static NSParagraphStyle* changeParagraphAlignment(NSParagraphStyle *p, NSTextAlignment align)
{
    if (p == nil) {
        p = [NSParagraphStyle defaultParagraphStyle];
    }
    NSMutableParagraphStyle *mp = [p mutableCopy];
    [mp setAlignment:align];
    return [mp autorelease];
}

NSDictionary* changeAttributesAlignment(NSDictionary *attrs, NSTextAlignment align)
{
    NSParagraphStyle *p = [attrs objectForKey:NSParagraphStyleAttributeName];
    NSMutableDictionary *result = [attrs mutableCopy];
    [result setObject:changeParagraphAlignment(p, align) forKey:NSParagraphStyleAttributeName];
    return [result autorelease];
}

@implementation MGPrintView
- (id)initWithPyParent:(id)pyParent
{
    self = [super initWithFrame:NSZeroRect];
    Class pyClass = [[self class] pyClass];
    PyObject *pParentRef = getHackedPyRef(pyParent);
    OBJP_LOCKGIL;
    Py_DECREF(pParentRef);
    OBJP_UNLOCKGIL;
    py = [[pyClass alloc] initWithParent:pParentRef];
    NSUserDefaults *ud = [NSUserDefaults standardUserDefaults];
    fontSize = [ud integerForKey:PrintFontSize];
    headerFont = [[NSFont boldSystemFontOfSize:fontSize] retain];
    headerAttributes = [NSDictionary dictionaryWithObjectsAndKeys:headerFont, NSFontAttributeName,
        [NSColor blackColor], NSForegroundColorAttributeName, nil];
    headerAttributes = [changeAttributesAlignment(headerAttributes, NSCenterTextAlignment) retain];
    baseTitle = [@"" retain];
    
    return self;
}

- (void)dealloc
{
    [py release];
    [headerFont release];
    [headerAttributes release];
    [baseTitle release];
    [super dealloc];
}

+ (Class)pyClass
{
    return [PyPrintView class];
}

- (PyPrintView *)py
{
    return py;
}

- (void)setUpWithPrintInfo:(NSPrintInfo *)pi
{
    NSRect pageBounds = [pi imageablePageBounds];
    [self setFrame:pageBounds];
    pageHeight = NSHeight(pageBounds);
    pageWidth = NSWidth(pageBounds);
    
    pageCount = 1;
    
    [baseTitle release];
    baseTitle = [[[self py] title] retain];
    baseHeaderTextHeight = [@"foo" sizeWithAttributes:headerAttributes].height;
    headerTextHeight = [baseTitle sizeWithAttributes:headerAttributes].height;
    headerHeight = headerTextHeight + 2;
}

- (void)drawRect:(NSRect)rect
{
    [super drawRect:rect];
    NSInteger pageNumber = [[NSPrintOperation currentOperation] currentPage];
    NSString *title = fmt(TR(@"%@ (Page %d of %d)"),baseTitle,pageNumber,pageCount);
    NSRect titleRect = NSMakeRect(rect.origin.x, rect.origin.y, rect.size.width, headerHeight);
    [title drawInRect:titleRect withAttributes:headerAttributes];
}
@end